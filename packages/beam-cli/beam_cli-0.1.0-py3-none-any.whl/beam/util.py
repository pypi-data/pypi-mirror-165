import requests
import shutil
import os


from http import HTTPStatus
from typing import Callable, Optional, Tuple
from itertools import repeat
from urllib.error import HTTPError
from multiprocessing.pool import ThreadPool
from rich.progress import Progress

DOWNLOAD_THREAD_COUNT = 8


def download_files(download_urls: dict, path: Optional[str] = None) -> bool:
    result_map = _async_pool(download_urls, _get_object, path=path)

    for _, success in result_map.items():
        if not success:
            return False

    return True


def safe_open(path: str, mode: str = "w"):
    """Open "path" for writing, creating any parent directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, mode)


def _async_pool(objects: dict, callback: Callable, path: Optional[str] = None) -> dict:
    result_map = {}

    with Progress() as progress:
        task = progress.add_task(
            "[green]Downloading sandbox files...", total=len(objects.keys())
        )

        for result in ThreadPool(DOWNLOAD_THREAD_COUNT).starmap(
            callback, zip(objects.items(), repeat(path))
        ):
            progress.advance(task)
            result_map[result[0]] = result[1]

    return result_map


def _get_object(object: Tuple, path: Optional[str] = None) -> Tuple:
    filename = object[0]
    url = object[1]

    if path is None:
        path = os.getcwd()

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        if response.status_code == HTTPStatus.OK:
            with safe_open(f"{path}/{filename}", "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)

    except (HTTPError, BaseException) as exc:
        return (filename, False)

    return (filename, True)
