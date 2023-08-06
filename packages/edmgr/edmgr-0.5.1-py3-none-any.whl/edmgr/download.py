from sys import stdout

from requests import get
from tqdm import tqdm

from edmgr.config import settings

L_BAR = "{desc}: {percentage:3.0f}%["
R_BAR = "] {n_fmt}/{total_fmt} {unit} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
BAR_FORMAT = f"{L_BAR}{{bar}}{R_BAR}"


def download_artifact(
    artifact_url: str, file_path: str, chunk_size: int = 1024
) -> None:

    with get(artifact_url, stream=True) as response_stream, open(
        file=file_path, mode="wb"
    ) as file, tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1000,
        total=int(response_stream.headers.get("content-length", 0)),
        file=stdout,
        bar_format=BAR_FORMAT,
        ascii=" -=",
        disable=settings.get("no_progress_bar", False),
    ) as bar:
        for chunk in response_stream.iter_content(chunk_size=chunk_size):
            data_size = file.write(chunk)
            bar.update(data_size)
