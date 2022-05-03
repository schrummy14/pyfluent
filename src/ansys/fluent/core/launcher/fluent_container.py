import os
import socket
import subprocess
import tempfile
import time
from typing import List


def _get_free_port() -> int:
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


def start_fluent_container(mounted_from: str, mounted_to: str, args: List[str]) -> int:
    """Start a Fluent container.

    Parameters
    ----------
    mounted_from : str
        Path to mount from. ``mounted_from`` will be mounted as ``mount_to``
        within the container.
    mounted_to : str
        Path to mount to. ``mounted_from`` will be mounted as ``mount_to``
        within the container.
    args : List[str]
        List of Fluent launch arguments

    Returns
    -------
    int
        gPRC server port exposed from container
    """
    fd, sifile = tempfile.mkstemp(suffix=".txt", prefix="serverinfo-", dir=mounted_from)
    os.close(fd)
    timeout = 100
    license_server = os.environ["ANSYSLMD_LICENSE_FILE"]
    port = _get_free_port()

    try:
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--rm",
                "-p",
                f"{port}:{port}",
                "-v",
                f"{mounted_from}:{mounted_to}",
                "-e",
                f"ANSYSLMD_LICENSE_FILE={license_server}",
                "-e",
                f"REMOTING_PORTS={port}/portspan=2",
                "-e",
                "FLUENT_LAUNCHED_FROM_PYFLUENT=1",
                "ghcr.io/pyansys/pyfluent",
                "-g",
                f"-sifile={sifile}",
            ]
            + args
        )

        sifile_last_mtime = os.stat(sifile).st_mtime
        while True:
            if os.stat(sifile).st_mtime > sifile_last_mtime:
                time.sleep(1)
                break
            if timeout == 0:
                break
            time.sleep(1)
            timeout -= 1
        return port
    except OSError:
        pass
    finally:
        if os.path.exists(sifile):
            os.remove(sifile)