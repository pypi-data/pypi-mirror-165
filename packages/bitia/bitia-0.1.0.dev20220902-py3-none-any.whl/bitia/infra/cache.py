__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import typing as T
import os
import threading
import time

import logging

from datetime import datetime
from functools import lru_cache
from urllib.parse import urlparse
from pathlib import Path
import requests

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from rich import print as rprint
from rich.progress import Progress

import typer

import bitia.config

# Progress bar
g_progress = Progress()


@lru_cache
def get_content_length(url: str) -> int:
    """Find content length of an url"""
    o = urlparse(url)
    if o.scheme == "ftp":
        from ftplib import FTP

        # FixMe: username, password
        ftp = FTP(o.netloc)
        ftp.login()
        return ftp.size(o.path) or -1

    res = requests.head(url, allow_redirects=True)
    return int(res.headers.get("content-length", -1))


def url2filepath(url: str, filename: T.Optional[str] = None) -> Path:
    """Given a url, determine its path in cache"""
    cachedir = bitia.config.cachedir()
    download_dir = cachedir / url
    if filename is None:
        o = urlparse(url)
        filename = o.fragment if o.fragment else Path(o.path).name
        assert filename, f"Could not determine the name of downloaded file from {o}"
    return download_dir / filename


def st_size(path: Path) -> int:
    if path.exists():
        return path.stat().st_size
    return -1


def download_if_not_in_cache(url: str, task) -> Path:
    global g_progress
    filepath_in_cache = url2filepath(url)
    filepath_in_cache.parent.mkdir(parents=True, exist_ok=True)

    remote_size = -1
    try:
        remote_size = get_content_length(url)
    except Exception as e:
        logging.warn(f"Failed to get the size of the file. Error was {e}")
        logging.warn("May be the network or server is down")
        if filepath_in_cache.is_file():
            logging.warn(
                """I found an old copy in the cache. I am going to
                    reuse it but makes not promise about correctness."""
            )

    assert remote_size > 0
    local_size = st_size(filepath_in_cache)
    if remote_size == local_size:
        logging.info(f"Already downloaded. {url} in cache. Reusing...")
        g_progress.update(task, update=1)
        return filepath_in_cache

    perc_done = 100.0 * local_size / remote_size
    if perc_done > 0:
        logging.info(
            f"Found {url} in cache ({perc_done:.2f}% complete). Continuing the download..."
        )

    download_file(url, filepath_in_cache)
    g_progress.update(task, update=1)
    assert filepath_in_cache.is_file()
    return filepath_in_cache


def show_download_progress(remote_size: int, filepath: Path):
    """A callback that monitors the progress of a file being downloaded."""
    size = st_size(filepath)
    while size < remote_size:
        time.sleep(5)
        size = st_size(filepath)
        perc_done = 100.0 * size / remote_size
        logging.info(f"File {filepath.name}: {perc_done:5.2f}% downloaded.")


def download_file(url: str, filepath: Path):
    """Download a given url and save content to the given filepath"""
    # Download and use a thread to monitor the progress.
    cachedir = bitia.config.cachedir()
    remote_size = get_content_length(url)
    t = threading.Thread(target=show_download_progress, args=(remote_size, filepath))
    t.start()
    logging.info(f"Downloading `{url}` to cache {cachedir}")
    _, retcode = bitia.common.run_blocking(
        f"wget --continue -o {filepath.name} {url}",
        cwd=filepath.parent,
    )
    t.join()
    assert retcode is not None


def cache_download(urls: T.List[str], *, workers: int) -> T.List[Path]:
    cachedir = bitia.config.cachedir()
    logging.info(f"Making file available in BiTIA cache :{cachedir}")
    res = []
    task = g_progress.add_task("Downloading...", total=len(urls))
    with g_progress:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            fs = [pool.submit(download_if_not_in_cache, url, task) for url in urls]
            for i, f in enumerate(concurrent.futures.as_completed(fs)):
                path_in_cache = f.result()
                assert path_in_cache.is_file()
                path_in_cwd = Path.cwd() / path_in_cache.name
                assert path_in_cwd.parent.is_dir()
                # symbolic link to cwd. If link already exists then remove it.
                if path_in_cwd.is_symlink():
                    os.remove(path_in_cwd)
                assert not path_in_cwd.is_file()
                os.symlink(path_in_cache, path_in_cwd)
                res.append(path_in_cache)
    return res


def make_available(urls_or_file: T.Union[str, Path]) -> T.List[Path]:
    """Download them in cache"""
    if Path(urls_or_file).exists():
        urls = Path(urls_or_file).read_text(encoding="utf-8").strip().split()
    else:
        urls = str(urls_or_file).split(",")

    numproc = 4
    if (k := os.cpu_count()) is not None:
        numproc = k + 1
    return cache_download(urls, workers=numproc)
