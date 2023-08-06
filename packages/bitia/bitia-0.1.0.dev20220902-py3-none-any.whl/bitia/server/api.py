__author__           = "Dilawar Singh"
__email__            = "dilawar@subcom.tech"


import typing as T

from bitia import __version__
from bitia.compose import ComposeFile
from bitia.server.model import Job

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/")
def hello():
    return dict(msg="Welcome to CoPR", version=__version__)


@app.post("/bootstrap")
def bootstrap_container(pkgnames: T.List[str], image: T.Optional[str] = None):
    """Setup a container that has given packages."""
    client = ComposeFile(pkgnames)
    return client.run(check=False)

@app.post("/submit")
def submit_job(job: Job):
    """Setup a container that has given packages."""
    client = ComposeFile(job.content)
    return StreamingResponse(client.run(check=False))
