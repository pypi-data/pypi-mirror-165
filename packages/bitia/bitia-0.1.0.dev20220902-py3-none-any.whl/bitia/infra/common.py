__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

from dataclasses import dataclass, field

import typing as T
import tarfile
from pathlib import Path

import bitia.config
import bitia.common


@dataclass
class ArtifactTar:
    """Generate a tar artifact from given files and message
    We add this artifact to the container when container is running.

    Example
    -------
    We may generate an script while installing a few package. This script(s) and
    associated command is passed to the container as tar file and command is
    added to `exec_run`.
    """

    cmd: str
    files_to_add: T.List[Path]
    location_in_container: Path = Path("/")
    location_in_host: Path = field(init=False)

    def __post_init__(self):
        """Prepare a tar archive"""

        # The tar file should preserve the filepath.
        h = bitia.common.hash256(self.cmd.encode())
        self.location_in_host = bitia.config.tempdir() / f"{h}.tar"
        with tarfile.open(self.location_in_host, "w") as tar:
            for path in self.files_to_add:
                path = path.resolve()
                tar.add(path)
        assert (
            self.location_in_host.exists()
        ), f"{self.location_in_host} does not exists"

    def exists(self):
        return self.location_in_host.exists()

    def path_host(self):
        return str(self.location_in_host)

    def path_container(self):
        return str(self.location_in_container)

    def data(self) -> bytes:
        return Path(self.path_host()).read_bytes()
