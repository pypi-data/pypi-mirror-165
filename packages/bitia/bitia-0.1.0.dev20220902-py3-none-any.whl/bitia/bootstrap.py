"""
Author        : Nitish Kumar
Email         : nitish.hbp@gmail.com

Describe      :

Copyright (C) 2022 Subconscious Compute 'All rights reserved.'
"""

import shutil
import subprocess
import tempfile

import distro
import typer

import bitia.config
import bitia.common

app = typer.Typer()

UID = bitia.config.uid()

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context) -> None:
    """Bootstrap this machine so that CoPR can run."""
    bootstrap_system()


def _which_distro_family() -> str:
    """Gets the name of Linux Distribution in lower case."""
    # FIXME: freedesktop_os_release is Python 3.10 only. Using distro library.
    return (distro.like() or distro.id()).lower()


def bootstrap_docker_or_podman():
    docker_or_podman = "docker"
    #while docker_or_podman not in ["docker", "podman"]:
    #    docker_or_podman = typer.prompt("Do you want to install docker or podman?")

    docker_or_podman_cli = shutil.which(docker_or_podman)
    if docker_or_podman_cli is not None:
        bitia.common.msg_check(f"{docker_or_podman} found at {docker_or_podman_cli}")
        return

    if UID != 0:
        assert (
            shutil.which("sudo") is not None
        ), "sudo is not installed, please install it on your system"

    _install_docker(_which_distro_family())


def _install_docker(os: str):
    script: str = ""
    if os == "debian":
        script = bitia.config.get_const('DOCKER_INSTALL_SCRIPT_DEB')
    elif os == "arch":
        script = bitia.config.get_const('DOCKER_INSTALL_SCRIPT_ARCH')
    else:
        typer.echo(
            f"{os} is not supported. Please use instructions from official page to install docker or podman."
        )
        return 

    if UID != 0:
        assert (
            shutil.which("sudo") is not None
        ), "sudo is not installed, please install it on your system"

    assert len(script.strip()) > 0
    bitia.common.run_shell(script)


# TODO: Refactor this
@app.command("bootstrap")
def bootstrap_system():
    """
    Bootstrap this system so that CoPR can execute pipelines.

    1. Installs docker or podman.
    """
    bootstrap_docker_or_podman()


if __name__ == "__main__":
    app()
