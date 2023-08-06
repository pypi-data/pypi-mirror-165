"""Management of packages and images."""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import shutil
import tempfile
import typing as T

from pathlib import Path
import logging

from bitia.common import run_blocking


class PackageManger:
    def __init__(self, name: str = "pacman"):
        self.name = name
        self.scripts: T.Dict[str, Path] = {}

    def install_command(self, pkg: str, non_interactive: bool = True) -> str:
        opts: str = ""
        install_str: str = "install"
        if non_interactive:
            if self.name == "pacman":
                opts = "--noconfirm --needed"
                install_str = "-Syu"
            else:
                logging.error(f"Not implemented for {self.name}")
        return f"{self.name} {opts} {install_str} {pkg}"

    def make_available_command(self, cmd: str, force_install: bool = False) -> str:
        """If a command not found then return a installation command that will
        make the command available. This is in beta and may not always work.
        """
        f = []
        f.append(f"if ! command -v {cmd} &> /dev/null; then")
        f.append(f"\techo '{cmd} is not found';")
        f.append(f"\tPKGNAME=$(pkgfile {cmd})")
        f.append("\t" + self.install_command("${PKGNAME}"))
        f.append("fi")
        return "\n".join(f)

    def gen_install_script(self, cmds: T.List[str]) -> str:
        txt = "#!/bin/sh\n"
        txt += "\n".join([self.make_available_command(cmd) for cmd in cmds])
        return txt

    def ensures(self, executables: T.List[str]):
        script = self.gen_install_script(executables)
        with tempfile.NamedTemporaryFile(
            mode="w", prefix="bitia", suffix=".sh", delete=False
        ) as f:
            f.write(script)
        run_blocking(f"sh {f.name}")
        Path(f.name).unlink(missing_ok=True)
