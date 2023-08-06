__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

__all__ = ["path2workdir", "str2workdir", "sniff_executales"]

from functools import lru_cache
from pathlib import Path
from bitia.common.checksumdir import dirhash
from bitia.common import hash256, bitia_workdir


def str2workdir(string: str) -> Path:
    return _hash2dir(hash256(string.encode()))


def path2workdir(path: Path) -> Path:
    """Given a path, return subdirectory for executing the pipeline. Read the
    content the of the directory and compute the hash. The hash is the name of
    the sub-directory.
    """
    return _hash2dir(_path2hash(path))


def get_workdir(user_input) -> Path:
    return (
        bitia_workdir() / path2workdir(user_input)
        if Path(user_input).exists()
        else bitia_workdir() / str2workdir(user_input)
    )


def _path2hash(path: Path) -> str:
    return str(dirhash(Path(path).resolve(), "sha256"))


def _hash2dir(hash: str) -> Path:
    return Path(hash[0:2]) / hash


def _sniff_info(main_script: Path):
    """Sniff metadata, directives and list of executables from the top-level script"""
    from bitia.common.script_sniffer import extract_info

    return extract_info(main_script.read_text())


@lru_cache
def sniff_executales(main_script: Path):
    """Sniff metadata, directives and list of executables from the top-level script"""
    return _sniff_info(main_script)["executable"]


def find_main_script(path: Path) -> Path:
    """Try to locate the top-level script in a given directory"""
    candidates = [x for x in path.glob("./*.bitia*") if x.is_file()]
    if candidates:
        assert (
            len(candidates) == 1
            ), f"More than one candidates are found for top-level script: {candidates}"
        return candidates[0]

    ## Try to find metadata 'bitia:main_script'
    # import mimetypes
    # all_textfiles = filter(path.glob('./*'), lambda x: 'text' in mimetypes.guess_type(x)[0])
    raise NotImplementedError("Search for candidate using metadata in file")
