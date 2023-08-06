"""Generate compose file."""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import shutil
import itertools
import collections
from pathlib import Path

import yaml
from jinja2 import Template

import logging

import bitia.common
import bitia.common.path

# Thanks https://stackoverflow.com/a/19323121/1805129
from yaml.representer import Representer

yaml.add_representer(collections.defaultdict, Representer.represent_dict)

DEFAULT_DOCKER_TEMPLATE = Template(
    """
FROM subcom/bitia:bioarchlinux
MAINTAINER bitia@subcom.tech

RUN python -m ensurepip
# RUN python -m pip install bitia --pre
RUN python -m pip install git+https://gitlab.subcom.tech/SubconsciousCompute/bitia 

WORKDIR {{ templ_workdir }}
#< RUN BEGINS
{{ templ_run_steps }}
#> RUN ENDS
"""
)


class ComposeFile(object):
    """Generates docker-compose file as well as Dockerfile to run this pipeline."""

    def __init__(self, user_input):
        assert user_input is not None
        # intialize the session dir. This changes the main_script_path as well.
        self.init_session_dir(user_input)
        assert self.session_dir.is_dir()
        assert self.main_script_path.is_file()

        self.dockerfile_path = self.default_dockerfile_path
        self.composefile_path = self.default_composefile_path
        self.compose = collections.defaultdict(dict)
        self.dockerfile_params = collections.defaultdict(str)
        self.init()

    def init(self):
        self.dockerfile_params["templ_workdir"] = "/app"
        self.compose["version"] = "3.0"
        self.compose["services"]["default"] = self.default_service()
        self.compose["volumes"] = self.init_volumes()

    def init_session_dir(self, user_input) -> Path:
        """Initialize the session directory. After that we work inside the
        session_dir only.
        """
        self.session_dir: Path = bitia.common.path.get_workdir(user_input)
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # Copy directories to session_dir if user_input is a filepath or a
        # directory.
        if (uinput := Path(user_input)).exists():
            if uinput.is_file():
                uinput = uinput.parent
            shutil.copytree(uinput, self.session_dir, dirs_exist_ok=True)

        # Copy is successful. Now set the `main_script_path`. If user_input is
        # file or directory then it just point to the session_director.
        if (uinput := Path(user_input)).exists():
            if uinput.is_file():
                self.main_script_path = self.session_dir / uinput.name
            else:
                # its a directory
                self.main_script_path = bitia.common.path.find_main_script(
                    self.session_dir
                )
                assert self.main_script_path.exists()
                assert self.main_script_path.is_file()
        else:
            # write a default script.
            self.main_script_path = self.default_script_path
            self.main_script_path.write_text(user_input)
        return self.session_dir

    @property
    def default_script_path(self) -> Path:
        p: Path = self.session_dir / ".bitia" / "__main__.sh"
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def default_dockerfile_path(self) -> Path:
        p: Path = self.session_dir / ".bitia" / "Dockerfile"
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def default_composefile_path(self) -> Path:
        p: Path = self.session_dir / "docker-compose.yaml"
        return p

    @property
    def container_workdir(self) -> str:
        wdir: str = str(self.dockerfile_params["templ_workdir"])
        return wdir

    def default_service(self):
        cachedir = bitia.config.cachedir()
        return dict(
            build=dict(context=".", dockerfile=str(self.dockerfile_path)),
            working_dir=self.container_workdir,
            volumes=[
                f"{self.session_dir}:{self.container_workdir}",
                f"{cachedir}:{cachedir}",
                "/tmp:/tmp",
            ],
            # ports=["3141:3141"],
        )

    def dockerfile_str(self) -> str:
        return DEFAULT_DOCKER_TEMPLATE.render(self.dockerfile_params)

    def init_volumes(self):
        return {}

    def __repr__(self):
        return yaml.dump(self.compose, sort_keys=False)

    def finalize(self):
        logging.info("Finalizing...")
        self.dockerfile_path.parent.mkdir(parents=True, exist_ok=True)
        with self.dockerfile_path.open("w") as f:
            logging.info(f"Writing Dockerfile {f.name}")
            f.write(self.dump_dockerfile())
        with self.composefile_path.open("w") as f:
            logging.info(f"Writing {f.name}")
            f.write(self.__repr__())

    def setup_docker_file(self):
        assert self.main_script_path is not None
        assert self.main_script_path.is_file()
        # TODO: Some more executables may be in the directives. We are not
        # extracting directives yet.
        executables = bitia.common.path.sniff_executales(self.main_script_path)
        assert executables, f"Empty list to install from {self.main_script_path}"
        self.dockerfile_params[
            "templ_run_steps"
        ] = f"RUN bitia tools ensure {' '.join(executables)}"

    def setup_compose_file(self):
        self.add_command(self._default_command())

    def add_command(self, command):
        """Add a command to compose file"""
        self.compose["services"]["default"]["command"] = command

    def container_path(self, path: Path) -> Path:
        """Map a local path to container path."""
        return self.container_workdir / path.relative_to(self.session_dir)

    def _default_command(self) -> str:
        assert self.main_script_path is not None
        exts = Path(self.main_script_path).suffixes
        # if there is shebang, honor it.
        path_in_container = self.container_path(self.main_script_path)
        with self.main_script_path.open() as f:
            first_line = str(f.readline())
        if first_line.startswith("#!"):
            return first_line.replace("#!", "").strip() + f" {path_in_container}"
        if ".py" in exts:
            return f"python {path_in_container}"
        if ".sh" in exts:
            return f"sh {path_in_container}"
        return f"sh {path_in_container}"

    def dump_dockerfile(self):
        return self.dockerfile_str()

    def populate_docker_files(self):
        """TODO: Docstring for populate_docker_files."""
        # TODO: Extract required installables from the user_input and create
        # docker file.
        self.setup_docker_file()
        # Setup docker-compose file to run the pipeline.
        self.setup_compose_file()

    def run(self, check: bool = False, recreate: bool = False, **kwargs):
        self.populate_docker_files()
        self.finalize()

        cmds = []
        if recreate:
            cmds += ["docker-compose down"]
            cmds += ["docker-compose build --no-cache"]

        if kwargs.get("versbose", False):
            # Add a command that shows information inside the container.
            pass

        args = "--no-color --abort-on-container-exit"
        cmds += [f"docker-compose up {args}"]

        bitia_cmds = [
            bitia.common.run_command(cmd, cwd=self.session_dir, check=check)
            for cmd in cmds
        ]
        return itertools.chain(*bitia_cmds)
