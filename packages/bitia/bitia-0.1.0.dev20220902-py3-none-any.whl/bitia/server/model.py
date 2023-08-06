"""Response model.

Reference
---------

- https://fastapi.tiangolo.com/tutorial/response-model/

"""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"


from enum import Enum

from pydantic import BaseModel


class JobType(Enum):
    Command = "command"
    Script = "script"
    Makefile = "makefile"
    Snakemake = "snakemake"


class Job(BaseModel):
    content: str
    type: JobType = JobType.Command

    def command(self) -> str:
        if self.type in [JobType.Script, JobType.Command]:
            return self.content
        raise NotImplementedError(f"{self.type} is not supported")
