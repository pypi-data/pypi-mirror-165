"""Configuration for CoPR

"""
__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"


import itertools
from dataclasses import dataclass
from pathlib import Path
import tempfile
import errno
import os
import typing as T

import bitia.common
import bitia.config.constants


@dataclass
class Config:
    # server = "https://bitia.zone:8000"
    server: str = "http://localhost:3141"


# Get the common file extensions. See Config in config.py that is responsible
# for updating this information dynamically using local file or REST api.
extension_tool_map: T.Dict[str, T.List[str]] = {
    "samtools": ["fq", "fai", "fa"],
    "seqtk": ["lst"],
    "samstat": ["sam", "bam", "fa"],
}


def get_all():
    return dict(tempdir=tempdir(), datadir=datadir(), cachedir=cachedir())


def tempdir() -> Path:
    """Return tempdir on this platform"""
    t = Path(tempfile.gettempdir())
    assert t.is_dir()
    return t


def datadir(create_if_doesnt_exist: bool = True) -> Path:
    """Return datadir to store temp data"""
    datadir = Path.home() / ".bitia"
    env_localdata = os.getenv("LOCALAPPDATA")
    if bitia.common.is_windows() and (env_localdata is not None):
        datadir = Path(env_localdata) / "bitia"
    if create_if_doesnt_exist:
        datadir.mkdir(parents=True, exist_ok=True)
    return datadir


def rundir() -> Path:
    """bitia executes the pipeline in this directory.

    If `BITIA_WORDIR` is not set, it is set to cwd() / 'bitia.output'
    """
    return workdir()

def workdir() -> Path:
    """bitia executes the pipeline in this directory.

    If `BITIA_WORDIR` is not set, it is set to cwd() / 'bitia.output'
    """
    return Path(os.environ.get("BITIA_WORDIR", Path.cwd() / "bitia.output"))


def is_writable(path: Path):
    """Test if a path is writable"""
    if not path.exists():
        return False
    try:
        testfile = tempfile.TemporaryFile(dir=str(path))
        testfile.close()
    except OSError as e:
        if e.errno == errno.EACCES:
            return False
        e.filename = path
        raise
    return True


def cachedir() -> Path:
    """Path where bitia keeps its downloaded cache. By default returns
    `/bitia_cache` if the user has permission to write here else return
    $HOME/.bitia/cache
    """
    cache = Path("/bitia_cache")
    # if the user doesn't have the permission to write to it, use one in user's
    # home.
    if is_writable(cache):
        return cache
    cache = datadir() / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    assert is_writable(cache)
    return cache


def supported_file_extensions() -> T.List[str]:
    """Get list of all supported files extensions."""
    return list(itertools.chain(*extension_tool_map.values()))


def tools_associated_with_extension(ext: str) -> T.List[str]:
    """Reverse lookup

    Examples
    --------

    >>> tools_associated_with_extension('fa')
    ['samtools', 'samstat']
    """
    global extension_tool_map
    tools: T.List[str] = []
    for tool, exts in extension_tool_map.items():
        if ext in exts:
            tools.append(tool)
    return tools


def get_const(key: str):
    return getattr(bitia.config.constants, key)


def uid() -> int:
    return int(get_const("UID"))


def gid() -> int:
    return int(get_const("GID"))


#
# Dynamic values.
#
config = Config()


def server() -> str:
    global config
    return config.server


def executor() -> str:
    return "docker"
