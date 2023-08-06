from logging import getLogger
import json
from typing import Optional, Union
import os

from msal import TokenCache
from requests import Response, HTTPError

from edmgr.requester import Requester
from edmgr.auth import (
    EdmAuthError,
    EdmTokenNotFound,
    msal_login,
    msal_logout,
    decode_jwt_token,
)
from edmgr.config import settings


logger = getLogger(__name__)


class EdmAPIError(Exception):
    pass


def _handle_response(response: Optional[Response]) -> Optional[dict]:
    if response is not None:
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            logger.debug(str(http_err))
            if response.status_code == 401:
                raise EdmAuthError("Unauthorized.")
            try:
                response_body = response.json()
            except json.JSONDecodeError as e:
                raise EdmAPIError(f"Cannot decode response body: {e}") from e
            if response_body.get("errorName"):
                return response_body
            raise
        try:
            response_body = response.json()
            if response_body:
                return response_body
        except json.JSONDecodeError as e:
            raise EdmAPIError(f"Invalid response body: {e}") from e


class Client:
    """
    client = Client()
    client = Client(token='token')
    client = Client(username='username', password='password')
    """

    def __init__(
        self,
        username: str = None,
        password: str = None,
        token: str = None,
        msal_cache: TokenCache = None,
        check_jwt_signature: bool = True,
        **kwargs,
    ) -> None:
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.__init_token: Optional[str] = token
        self.__token: Optional[str] = None
        self.__msal_cache: Optional[TokenCache] = msal_cache
        self._check_jwt_signature = check_jwt_signature
        self.__kwargs = kwargs
        entitlements_endpoint = os.path.join(
            settings.get("base_url"), settings.get("entitlement_endpoint")
        )
        self.entitlements_api = Requester(
            base_url=entitlements_endpoint,
            timeout=kwargs.get("timeout"),
            raise_request_exc=kwargs.get("raise_request_exc"),
        )
        self._acquire_token(timeout=kwargs.get("timeout"), allow_null=True)

    @property
    def token(self) -> Optional[str]:
        return self.__token

    @token.setter
    def token(self, token: str) -> None:
        self._set_token(token, check_signature=self._check_jwt_signature)

    def _set_token(self, token: str, check_signature: bool = True) -> dict:
        payload = decode_jwt_token(token, check_signature=check_signature)
        self.__token = token
        self.entitlements_api.token = token
        return payload

    def _acquire_token(
        self, timeout: Union[float, tuple] = None, allow_null: bool = False
    ) -> None:
        # If the current instance has a valid token already, do nothing
        if self.__token is not None:
            try:
                self._set_token(self.__token, check_signature=False)
                return
            except EdmAuthError:
                pass
        # otherwise, if the current instance was instanciated with a token, use it
        if self.__init_token is not None:
            self._set_token(
                self.__init_token, check_signature=self._check_jwt_signature
            )
        # otherwise, if an access token is set in the config module, use it
        elif settings.get("access_token") is not None:
            self._set_token(
                settings["access_token"], check_signature=self._check_jwt_signature
            )
        # otherwise, get an access token from msal:
        #   - if username and password are provided and the token is expired, a
        #     new one will be acquired
        #   - if no username and password are provided, self.__msal_cache will
        #     be used to acquire the token
        #   - if no user/password or msal_cache is empty/invalid, raise EdmAuthError
        elif (self.username is not None and self.password is not None) or (
            self.__msal_cache is not None
        ):
            access_token = msal_login(
                username=self.username,
                password=self.password,
                timeout=timeout,
                cache=self.__msal_cache,
            )
            self._set_token(access_token, check_signature=False)
        elif not allow_null:
            raise EdmTokenNotFound("Access token not found.")

    def logout(self):
        """Sign out, remove accout from MSAL cache and remove access token from Client"""
        if self.__msal_cache is not None:
            msal_logout(self.__msal_cache)
            self.__msal_cache = TokenCache()
        self.__token = None

    def get_entitlements(
        self, entitlement_id: int = None, params: dict = None, **kwargs
    ) -> list:
        """
        Call the entitlements API and get a list of entitlements

        :param entitlement_id: Entitlement ID
        :param params: Query params
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: a list of entitlements
        """
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))
        if entitlement_id is not None:
            url = str(entitlement_id)
        else:
            url = ""
        response: Optional[Response] = self.entitlements_api.get(url, params, **kwargs)

        data: Optional[dict] = _handle_response(response)

        if data:
            if entitlement_id is not None:
                return [data]
            return data.get("items", [])
        return []

    def get_releases(
        self, entitlement_id: int, release_id: str = None, params: dict = None, **kwargs
    ) -> list:
        """
        Call the entitlements API with the entitlement ID to get a list of product releases

        :param entitlement_id: Entitlement ID
        :param release_id: Release ID
        :param params: Query params
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: a list of product releases
        """
        logger.debug(f"get_releases {kwargs}")
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))

        parts = [f"{entitlement_id}/rights/download/releases"]
        if release_id is not None:
            parts.append(release_id)
        url = "/".join(parts)
        response: Optional[Response] = self.entitlements_api.get(url, params, **kwargs)

        data: Optional[dict] = _handle_response(response)

        if data:
            if release_id is not None:
                return [data]
            return data.get("items", [])
        return []

    def get_artifacts(
        self, entitlement_id: int, release_id: str, artifact_id: str = None, **kwargs
    ) -> list:
        """
        Call the entitlements API with the entitlement ID and release ID to get a list of artifacts
        :param entitlement_id: entitlement ID
        :param release_id: release ID
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: a list of artifacts
        """
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))

        parts = [f"{entitlement_id}/rights/download/releases/{release_id}"]
        if artifact_id is not None:
            parts.append(f"artifact/{artifact_id}")
        url = "/".join(parts)
        response: Optional[Response] = self.entitlements_api.get(url, **kwargs)
        data: Optional[dict] = _handle_response(response)

        if data:
            if artifact_id is not None:
                return [data]
            return data.get("artifacts", [])
        return []

    def get_artifact_download_url(
        self, entitlement_id: int, release_id: str, artifact_id: str, **kwargs
    ) -> Optional[dict]:
        """
        Call the entitlements API with the entitlement ID, release ID, and artifact_id to get a of artifact's download url
        Then filters based on Artifact ID
        :param artifact_id: artifact ID
        :param entitlement_id: entitlement ID
        :param release_id: release ID
        :raises EdmAPIError: If the response body is not a valid JSON
        :raises EdmAuthError: If token is not authorized
        :raises requests.HTTPError: For any unexpected HTTP Error response
        :return: None or a list of artifacts
        """
        kwargs = {**self.__kwargs, **kwargs}
        self._acquire_token(timeout=kwargs.get("timeout"))
        response: Optional[Response] = self.entitlements_api.get(
            f"{entitlement_id}/rights/download/releases/{release_id}/artifact/{artifact_id}/http",
            **kwargs,
        )
        data: Optional[dict] = _handle_response(response)

        return data
