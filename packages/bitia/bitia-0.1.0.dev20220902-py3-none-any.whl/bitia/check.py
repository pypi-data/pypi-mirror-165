"""
Performs various checks.


Authors
-------

- Nitish Kumar
- Dilawar Singh <dilawar@subcom.tech>

© 2022- , Subconscious Compute, All rights reserved.
"""

import shutil
from pathlib import Path

import bitia.common

import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context) -> None:
    """Check the installation and setup."""
    check_all()


def check_docker_podman():
    """check to see if `docker/podman run hello-world' succeeds or not"""
    docker_exec = shutil.which("docker")
    podman_exec = shutil.which("podman")

    if podman_exec is not None:
        bitia.common.msg_check(f"podman is installed. Found at {podman_exec}.")
    elif docker_exec is not None:
        bitia.common.msg_check(f"docker is installed. Found at {docker_exec}.")
    else:
        bitia.common.msg_cross(
            "docker/podman not installed, please run `bitia bootstrap`"
        )
        return

    check_exe = podman_exec or docker_exec
    typer.echo(f"Checking {check_exe}")
    for line in bitia.common.run_command(
        f"{check_exe} run hello-world", cwd=Path.cwd()
    ):
        print(line)
    bitia.common.msg_check(f"{check_exe} is functional. yay!")


# This is the default command. It is executed when `bitia check` is called
# without any subcommmand name. It is done using `callback`. See
# https://typer.tiangolo.com/tutorial/commands/callback/
@app.command("all")
def check_all():
    """
    check if all required tools are installed.
    """
    check_docker_podman()


if __name__ == "__main__":
    app()
