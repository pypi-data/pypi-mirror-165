from _typeshed import Incomplete
from typing import NamedTuple
from ujenkins.endpoints import Builds as Builds, Jobs as Jobs, Nodes as Nodes, System as System, Views as Views
from ujenkins.exceptions import JenkinsError as JenkinsError, JenkinsNotFoundError as JenkinsNotFoundError

class Response(NamedTuple):
    status: Incomplete
    headers: Incomplete
    body: Incomplete

class Jenkins:
    builds: Incomplete
    jobs: Incomplete
    nodes: Incomplete
    system: Incomplete
    views: Incomplete
    def __init__(self) -> None: ...
