"""
Copyright (C) 2022 Subconscious Compute 'All rights reserved.'

The background service to setup infrastructure.
"""

import typing as T
import sys
import signal
import time
from datetime import datetime

from pid import PidFile

import daemon
import psutil

import bitia.common as cc

import typer

app_cli = typer.Typer()


def cleanup():
    pass


def reload_config():
    pass


@app_cli.command("start")
def start(port: int = 3141):
    """Run the server"""
    import uvicorn

    # check if the port is already in use.
    if cc.is_port_in_use(port):
        cc.msg_cross(f"port {port} is in use. Please use a different port")
        return

    # https://peps.python.org/pep-3143/ and python-daemon file.
    # also see https://github.com/trbs/pid/
    context = daemon.DaemonContext(
        stderr=sys.stderr,
        working_directory=str(cc.bitia_workdir()),
        pidfile=PidFile(str(cc.pidfile())),
    )

    context.signal_map = {
        signal.SIGTERM: cleanup,
        signal.SIGHUP: "terminate",
        signal.SIGUSR1: reload_config,
    }

    with context:
        uvicorn.run("bitia.server.api:app", host="0.0.0.0", port=port)
        time.sleep(1)
        cc.msg_check(f"Server is running at http://localhost:{port}.")


def _get_server_pid() -> T.Optional[int]:
    if not cc.pidfile().exists():
        return None

    # read the pid from the pid file and get handle on the process.
    pid = int(cc.pidfile().read_text())
    if psutil.pid_exists(pid):
        return pid
    return None


@app_cli.command("status")
def status():
    """Report the status of the server"""

    typer.echo("Checking the status of the server")
    pid = _get_server_pid()
    if pid is None:
        typer.echo("Server is not running. Use `bitia server start`")
        return

    pinfo = psutil.Process(pid)
    started = datetime.fromtimestamp(pinfo.create_time()).strftime("%Y-%m-%d %H:%M:%S")
    cc.msg_check(
        f"server is running: pid={pid}, status={pinfo.status()}, started={started}."
    )


@app_cli.command("stop")
def stop():
    """Report the status of the server"""

    pid = _get_server_pid()
    if pid is None:
        typer.echo("Server is not running.")
        return

    p = psutil.Process(pid)
    p.terminate()
    time.sleep(4)
    if _get_server_pid() is None:
        cc.msg_check("Successfully stopped.")
        return
    cc.msg_cross("Failed to terminate the server.")
