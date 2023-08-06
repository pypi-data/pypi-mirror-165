"""
Welcome to CoPR (Complex Pipeline Runner).

©2022 - Subconscious Compute 'All rights reserved.'
"""

import logging
import os

import typing as T

import bitia.infra.cache
import bitia.common
import bitia.run
import typer

app = typer.Typer()


import bitia.bootstrap

app.add_typer(bitia.bootstrap.app, name="bootstrap")

import bitia.check

app.add_typer(bitia.check.app, name="check")

import bitia.tools

app.add_typer(bitia.tools.app, name="tools")


import bitia.server.main

app.add_typer(bitia.server.main.app_cli, name="server")

@app.command("config")
def config():
    """Show configuration"""
    import bitia.config 

    print(bitia.config.get_all())

# NOTE: typer does not support Union Type yet.
@app.command("run")
def run_user_input(
    user_input: str,
    server: T.Optional[str] = None,
    recreate: bool = False,
    verbose: bool = False,
):
    """runs the passed command or file inside a docker container and returns the output

    Parameteres
    -----------
    user_input : str
        It could be a command, a directory or a file path.
    server : str, optional
        Gets the server address from the user.
    recreate: bool, default `False`
        If `True`, force receation of the container.
    vernose: bool, default `False`
        If `True`, run in the verbose mode.

    Returns
    -------
    None

    See Also
    --------
    bitia.daemon.daemon

    """
    bitia.run.submit_job(user_input, server=server, recreate=recreate, verbose=verbose)


if __name__ == "__main__":
    app()
