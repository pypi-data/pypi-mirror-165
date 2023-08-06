__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import os
import tempfile
import platform
import sys
import shutil
import logging
import glob
import subprocess
from enum import Enum

from rich import print as rprint

import typer

import typing as T

from pathlib import Path

import bitia.config


class Executor(str, Enum):
    """Supported executors"""

    podman = "podman"
    docker = "docker"
    bash = "bash"
    sh = "sh"
    shell = "shell"


def system() -> T.Tuple[str, str]:
    return (platform.system(), sys.platform)


def is_windows(cygwin_is_windows: bool = True) -> bool:
    """Check if we are running on windows.

    Parameters
    ----------
        cygwin_is_windows : (default `True`). When set to `True`, consider cygwin as Windows.

    Returns
    -------
    `True` if on Windows, `False` otherwise.
    """
    _sys = system()
    if _sys[0].startswith("windows"):
        return True
    return cygwin_is_windows and _sys[1] == "cygwin"


def find_program(
    name: str, hints: T.List[T.Union[Path, str]] = [], recursive: bool = False
) -> T.Optional[str]:
    """where is a given binary"""
    for hint in hints:
        hint = Path(hint).resolve()
        if not hint.exists():
            continue
        for p in glob.glob(f"{hint}/**/{name}", recursive=recursive):
            prg = shutil.which(p)
            if prg is not None:
                return prg
    return shutil.which(name)


def msg_check(msg: str):
    typer.echo(f"✓ {msg}")
    sys.stdout.flush()


def msg_cross(msg: str):
    typer.echo(f"❌ {msg}")
    sys.stdout.flush()


def run_shell(script: str, shell: str = "sh", remove_after_execution: bool = True):
    """Run a shell script

    TODO: Replace this with xonsh.
    """
    shellcmd = shutil.which(shell)
    assert shellcmd is not None
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".sh", prefix="bitia_", delete=False
    ) as f:
        f.write(script)
        return run_blocking(f"{shellcmd} -c {f.name}")


def run_blocking(
    cmd: str, cwd: Path = Path.cwd(), silent: bool = False
) -> T.Tuple[str, T.Optional[int]]:
    """Run a given command in blocking mode. Return the output and and status
    code.

    if `silent` is False, write the output onto console.
    """
    lines = []
    retcode: T.Optional[int] = None
    for (output, retcode) in _run_command(cmd, cwd=cwd):
        if output:
            lines.append(output)
            if not silent:
                rprint(output)
    return "\n".join(output), retcode


def run_command(cmd: str, *, cwd, check: bool = True
) -> T.Generator[str, None, T.Optional[int]]:
    """Run a given command and stream its output. The last value is the return
    code of the command.

    Parameters
    ----------
    cmd : str
        cmd
    cwd : Path
        Current working directory.
    check: bool
        Check if return code is 0. if not throws an exception.

    Credits
    --------
    1. https://stackoverflow.com/questions/18421757/live-output-from-subprocess-command
    """
    retcode: T.Optional[int] = None
    for (output, retcode) in _run_command(cmd, cwd=cwd):
        if output:
            yield output
    if check:
        assert retcode is not None
        assert retcode == 0, f"Command did not execute successfully. retcode {retcode}."
    return retcode


def _run_command(cmd: str, *, cwd) -> T.Generator[T.Tuple[str, T.Optional[int]], None, None]:
    logging.info(f"Executing '{cmd}' in {cwd}")
    p = subprocess.Popen(
        cmd.split(),
        text=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if p.stdout is not None:
        for line in iter(p.stdout.readline, ""):
            if line is None:
                break
            yield (line.rstrip(), None)
    p.poll()
    yield ("", p.returncode)


def hash256(data: bytes) -> str:
    """Compute the hash of a given string."""
    import hashlib

    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest()


def is_port_in_use(port: int) -> bool:
    """Check if a given port is in use.

    Credit
    ------
    Thanks https://stackoverflow.com/a/52872579/1805129
    """
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
    return False


def user() -> str:
    """Return current user name"""
    return str(os.getenv("USER"))


def pidfile() -> Path:
    return bitia.config.datadir(True) / "bitia.pid"


def bitia_workdir() -> Path:
    """Work directory of the server"""
    return bitia.config.datadir(True)
