#!/usr/bin/env python

import functools
import json
import logging
from pathlib import Path
import sys
from time import localtime, strftime
from typing import Optional, Union

from click import (
    confirm,
    echo,
    style,
    group,
    option,
    argument,
    password_option,
    Choice,
)
from msal import SerializableTokenCache
from msal.exceptions import MsalError
from requests.exceptions import RequestException
from tabulate import tabulate

from edmgr.client import Client, EdmAPIError
from edmgr import auth
from edmgr import download
from edmgr.config import get_log_level_from_verbose, settings


logger = logging.getLogger(__name__)


ASCII_ART = """
███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██╔████╔██║
██╔══╝  ██║  ██║██║╚██╔╝██║
███████╗██████╔╝██║ ╚═╝ ██║
╚══════╝╚═════╝ ╚═╝     ╚═╝
"""

CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: x.lower())


def echo_error(msg: str) -> None:
    echo(style(text=msg, fg="red", bold=True), err=True)


def echo_alert(msg: str) -> None:
    echo(style(text=msg, fg="yellow", bold=False))


def echo_info(msg: str) -> None:
    echo(style(text=msg, fg="green", bold=True))


def exception_handler(exc: Exception):
    if isinstance(exc, auth.EdmTokenNotFound) or isinstance(exc, auth.EdmTokenExpired):
        msg = (
            f"{exc}\nPlease login using `edmgr login` "
            "or set EDM_ACCESS_TOKEN environment variable to a valid token."
        )
        return echo_error(msg)
    if isinstance(exc, auth.EdmAuthError) or isinstance(exc, MsalError):
        return echo_error(f"Authentication error: {exc}")
    if isinstance(exc, RequestException) or isinstance(exc, EdmAPIError):
        return echo_error(f"API Error: {exc}")
    logger.debug(f"Unexpected {type(exc)}: {exc}")
    return echo_error(f"Error: {exc}")


def convert_bytes_size(
    bytes_size: int, system: str = "metric", decimal_places: int = 3
) -> str:
    """
    Helper function to convert sizes from bytes into bytes multiples, in order to be
    human readable.

    :param bytes_size: file size
    :param system: the conversion system, either metric or binary. Default metric
    :param decimal_places: decimal places to return. Default 3
    :return: file size converted
    """
    size = int(bytes_size)
    if system == "metric":
        factor = 1000
        units = ("B", "kB", "MB", "GB", "TB", "PB")
    elif system == "binary":
        factor = 1024
        units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")
    else:
        raise ValueError("Invalid conversion system")
    for unit in units:
        if size < factor:
            break
        size /= factor
    display = f"{size:.{decimal_places}f}".rstrip("0").rstrip(".")
    return f"{display} {unit}"


def print_local_time(timestamp: Union[float, int]) -> str:
    return strftime("%a, %d %b %Y %H:%M:%S", localtime(int(timestamp)))


def filter_entitlement(entitlement: dict) -> dict:
    quality: str = ", ".join(
        [e.get("quality") for e in entitlement.get("rights", {}).get("qualities", {})]
    )
    allowed_countries = "\n".join(
        [
            f"{country.get('id', 'None').upper()} - {country.get('uri')}"
            for country in entitlement.get("compliance", {}).get("allowedCountries", {})
        ]
    )
    return {
        "Entitlement Id": entitlement.get("id"),
        "Product Code": entitlement.get("product", {}).get("id"),
        "Status": entitlement.get("status"),
        "Right To": entitlement.get("rightTo"),
        "Valid From": entitlement.get("validFrom"),
        "Valid To": entitlement.get("validTo"),
        "Qualities": quality,
        "Compliance Status": entitlement.get("compliance", {}).get("status"),
        "Allowed Countries": allowed_countries,
        # TODO: Where is Contract coming from?
        # 'Contract': 'See TODO comment in edmgrcli'
    }


def filter_release(release: dict) -> dict:
    return {
        "Entitlement Id": release.get("entitlement", {}).get("id"),
        "Release Id": release.get("id"),
        "Release Name": release.get("name"),
        "Revision": release.get("revision"),
        "Patch": release.get("patch"),
        "Major Version": release.get("majorVersion"),
        "Minor Version": release.get("minorVersion"),
        "Quality": release.get("quality"),
        "Type": release.get("type"),
        "Available At": release.get("availableAt"),
    }


def filter_artifact(artifact: dict) -> dict:
    bytes_size = artifact.get("fileSize")
    file_size = convert_bytes_size(bytes_size) if bytes_size is not None else None
    return {
        "Artifact Id": artifact.get("id"),
        "Name": artifact.get("name"),
        "Description": artifact.get("description"),
        "Type": artifact.get("type"),
        "File Name": artifact.get("fileName"),
        "File Size": file_size,
        "MD5": artifact.get("md5"),
    }


def cli_output(filter_function, records, **kwargs) -> None:
    if kwargs.get("format") != "table":
        indent = None
        sort_keys = False
        if kwargs.get("format") == "jsonpp":
            indent = 4
            sort_keys = True
        echo(json.dumps(records, indent=indent, sort_keys=sort_keys))
    else:
        output = [filter_function(record) for record in records]

        echo(tabulate(output, headers="keys", tablefmt="fancy_grid"))


def pagination_params(offset: int, limit: int) -> dict:
    if offset is not None:
        return {"offset": offset, "limit": limit}
    return {}


def get_client() -> Client:
    """
    Load access token from disk cache if found and return a Client instance
    instanciated with either a JWT token or a MSAL TokenCache.

    JWT string cache takes precedence if found, otherwise cached MSAL TokenCache
    is used if found.

    If no cache file is found, return a Client instance with no arguments, the
    Client will use the token found in settings.

    :return: Client instance
    """
    token = auth.get_jwt_cache()
    if token:
        logger.debug("Cached JWT token found")
        return Client(token=token)
    msal_cache = auth.get_msal_cache()
    if msal_cache:
        logger.debug("Cached MSAL cache found")
        return Client(msal_cache=msal_cache)
    return Client()


def logout_and_clear_cache():
    cache = auth.get_msal_cache()
    if cache is not None:
        auth.msal_logout(cache)
    auth.delete_cache()


def common_options(command_func):
    @option(
        "-f",
        "--format",
        type=Choice(["table", "json", "jsonpp"], case_sensitive=False),
        default="table",
        show_default=True,
        help="Output format -> tabular, json or json prettify",
    )
    @functools.wraps(command_func)
    def common_options_wrapper(*args, **kwargs):
        return command_func(*args, **kwargs)

    return common_options_wrapper


def main():
    try:
        cli()
    except Exception as e:
        exception_handler(e)
        sys.exit(1)


@group()
@option(
    "-k",
    "--environment",
    type=Choice(["prod", "sandbox", "qa"], case_sensitive=False),
    default="prod",
    show_default=True,
    help="Configuration environment",
)
@option("-v", "--verbose", count=True)
def cli(environment, verbose):
    settings.set_env(environment.upper())

    if verbose:
        verbosity = min(verbose, 3)
        settings["log_level"] = get_log_level_from_verbose(verbosity)

    logging.basicConfig(
        level=settings["log_level"],
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s - : %(message)s",
        datefmt="%m-%d %H:%M:%S",
    )


@cli.command(context_settings=CONTEXT_SETTINGS, help="Print configuration")
def show_config():
    echo(json.dumps(settings._env, indent=4, sort_keys=True))


@cli.group(help="Login using credentials/token")
def login():
    pass


@login.command(
    context_settings=CONTEXT_SETTINGS, help="Login using username and password"
)
@option(
    "-u",
    "--username",
    type=str,
    prompt=True,
    required=True,
    help="Username (email) used for logging on to Arm",
)
@password_option(
    required=True, confirmation_prompt=False, help="Password used for logging on to Arm"
)
def credentials(username: str, password: str):
    logout_and_clear_cache()
    echo(style(text="Logging in, please wait...", fg="yellow", bold=False))
    msal_cache = SerializableTokenCache()
    auth.msal_login(username=username, password=password, cache=msal_cache)
    auth.save_msal_cache(msal_cache)

    echo(ASCII_ART)
    echo_info("Logged in successfully")


@cli.command(context_settings=CONTEXT_SETTINGS, help="Logout by deleting cached token")
def logout():
    logout_and_clear_cache()
    echo_info("Successfully logged out and cached token removed")


@login.command(
    context_settings=CONTEXT_SETTINGS,
    help="Login using JWT string",
)
@argument("token")
def token(token: str):
    logout_and_clear_cache()
    auth.decode_jwt_token(token)
    auth.save_jwt_cache(token)

    echo_info(f"Token saved in {settings['edm_root']}")


@login.command(
    context_settings=CONTEXT_SETTINGS,
    help="Print Access Token as JWT string with some extra information.",
)
def show_token():
    client = get_client()
    token = client.token
    payload = auth.decode_jwt_token(token, check_signature=False, check_claims=False)

    msg = (
        "Token attained:"
        f"\n  - Token Owner: {payload.get('given_name')} {payload.get('family_name')}"
        f"\n  - Email: {payload.get('emails')}"
        f"\n  - Expires: {print_local_time(payload.get('exp'))}"
        f"\n  - Access Token: {token}"
    )
    echo_info(msg)


@cli.command(
    context_settings=CONTEXT_SETTINGS, help="Print a list of available entitlements."
)
@option("-e", "--entitlement-id", type=int, help="Entitlement ID to retrieve one")
@option("-o", "--offset", type=int, help="Page number to paginate output")
@option(
    "-l",
    "--limit",
    type=int,
    default=10,
    help="Number of records per page to be displayed. By default it shows 10 records per page",
)
@common_options
def entitlements(entitlement_id: int = None, **kwargs):
    client = get_client()
    params = {}
    params.update(pagination_params(kwargs.get("offset"), kwargs.get("limit")))
    entitlements: Optional[list] = client.get_entitlements(
        entitlement_id=entitlement_id, params=params, **kwargs
    )
    if entitlements:
        return cli_output(filter_entitlement, entitlements, **kwargs)
    if entitlement_id:
        return echo_error("Couldn't find Entitlement with the given Entitlement ID")
    echo_error("Couldn't find any Entitlements")


@cli.command(
    context_settings=CONTEXT_SETTINGS,
    help="Print a list of releases for a particular entitlement.",
)
@option(
    "-e",
    "--entitlement-id",
    type=int,
    prompt=True,
    required=True,
    help="Entitlement ID",
)
@option("-r", "--release-id", type=str, help="Release ID to retrieve one")
@common_options
def releases(entitlement_id: int, release_id: str = None, **kwargs):
    client = get_client()
    releases: Optional[list] = client.get_releases(
        entitlement_id=entitlement_id, release_id=release_id, **kwargs
    )
    if releases:
        return cli_output(filter_release, releases, **kwargs)
    if release_id:
        return echo_error(
            "Couldn't find Release with the given Entitlement ID & Release ID"
        )
    echo_error("Couldn't find any Release with the given Entitlement ID")


@cli.command(
    context_settings=CONTEXT_SETTINGS,
    help="Print a list of artifacts for a particular release.",
)
@option(
    "-e",
    "--entitlement-id",
    type=int,
    prompt=True,
    required=True,
    help="Entitlement ID",
)
@option("-r", "--release-id", type=str, prompt=True, required=True, help="Release ID")
@option("-a", "--artifact-id", type=str, help="Artifact ID to retrieve one")
@common_options
def artifacts(entitlement_id: int, release_id: str, artifact_id: str = None, **kwargs):
    client = get_client()
    artifacts: Optional[list] = client.get_artifacts(
        entitlement_id=entitlement_id,
        release_id=release_id,
        artifact_id=artifact_id,
    )
    if artifacts:
        return cli_output(filter_artifact, artifacts, **kwargs)
    if artifact_id:
        return echo_error(
            "Couldn't find artifact with the given Entitlement ID, Release ID & Artifact ID"
        )
    echo_error("Couldn't find any artifacts with the given Entitlement ID & Release ID")


@cli.command(
    context_settings=CONTEXT_SETTINGS,
    help="Download all artifacts for a particular release or only a specific one.",
)
@option(
    "-e",
    "--entitlement-id",
    type=int,
    prompt=True,
    required=True,
    help="Entitlement ID",
)
@option("-r", "--release-id", type=str, prompt=True, required=True, help="Release ID")
@option("-a", "--artifact-id", type=str, help="Artifact ID")
@option(
    "-d",
    "--download-dir",
    type=str,
    help="Directory in which artifacts are downloaded. Default: $HOME/Artifacts",
)
def download_artifacts(
    entitlement_id: int,
    release_id: str,
    artifact_id: str = None,
    download_dir: str = None,
):
    client = get_client()
    artifacts: Optional[dict] = client.get_artifacts(
        entitlement_id=entitlement_id,
        release_id=release_id,
        artifact_id=artifact_id,
    )

    if not download_dir:
        download_dir = settings["downloads"]

    download_dir = Path(download_dir).expanduser()
    download_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    if not artifacts:
        return echo_error(
            f"No artifact found for Entitlement ID: {entitlement_id} and Release ID: {release_id}"
        )

    for artifact in artifacts:
        file_name = artifact.get("fileName")
        art_id = artifact.get("id")
        if not file_name:
            echo_error(f"API Error: Invalid artifact fileName: {file_name}")

        download_url: Optional[dict] = client.get_artifact_download_url(
            entitlement_id=entitlement_id, release_id=release_id, artifact_id=art_id
        )
        while (
            download_url
            and download_url.get("errorName") == "download-error-eula-required"
        ):
            echo_error(f"{download_url['errorDescription']}.")
            echo(
                "Please sign the EULA at the following link, then proceed or abort the download."
            )
            echo()
            echo(download_url["agreementUrl"])
            echo()
            confirm(
                "Do you want to proceed with the download?", default=True, abort=True
            )
            download_url = client.get_artifact_download_url(
                entitlement_id=entitlement_id, release_id=release_id, artifact_id=art_id
            )

        if not download_url:
            echo_error(
                "Couldn't find download URL for"
                f" Entitlement ID: {entitlement_id}, Release ID: {entitlement_id} and Artifact ID: {art_id}"
            )

        if not download_url.get("downloadUrl"):
            return echo_error("API Error: Invalid downloadUrl")

        file_path = (Path(download_dir) / file_name).resolve()
        echo(f"Downloading {file_path}")
        download.download_artifact(
            artifact_url=download_url["downloadUrl"],
            file_path=file_path,
        )
    echo_info("All done!")


if __name__ == "__main__":
    main()
