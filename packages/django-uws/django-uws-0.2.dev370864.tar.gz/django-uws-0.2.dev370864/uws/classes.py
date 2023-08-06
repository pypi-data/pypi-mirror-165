""" Python classes to represent UWS objects """

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class UWSParameter:
    """UWS Parameter Python object"""

    key: str
    value: str
    byReference: bool = False
    isPost: bool = False


@dataclass(frozen=True)
class UWSResult:
    """UWS Result Python object"""

    key: str
    value: str
    size: Optional[int] = None
    mimeTime: Optional[str] = None


class UWSJob:
    """UWS Job Python object

    Maps a dictionary to a Python object with attributes
    """

    def __init__(self, data: dict):
        self._url = data["url"]
        self._jobId = data["jobId"]
        self._runId = data["runId"]
        self._ownerId = data.get("ownerId", None)
        self._phase = data["phase"]
        self._quote = data.get("quote", None)
        self._creationTime = data.get("creationTime", None)
        self._startTime = data.get("startTime", None)
        self._endTime = data.get("endTime", None)
        self._executionDuration = data.get("executionDuration", 0)
        self._destruction = data.get("destruction", None)
        self._errorSummary = data.get("errorSummary", None)

        self._parameters = [UWSParameter(**p) for p in data["parameters"]]
        self._results = [UWSResult(**r) for r in data["results"]]

    @property
    def url(self) -> str:
        return self._url

    @property
    def jobId(self) -> str:
        return self._jobId

    @property
    def runId(self) -> str:
        return self._runId

    @property
    def ownerId(self) -> str:
        return self._ownerId

    @property
    def phase(self) -> str:
        return self._phase

    @property
    def quote(self) -> datetime:
        return self._quote

    @property
    def creationTime(self) -> datetime:
        return self._creationTime

    @property
    def startTime(self) -> datetime:
        return self._startTime

    @property
    def endTime(self) -> datetime:
        return self._endTime

    @property
    def executionDuration(self) -> int:
        return self._executionDuration

    @property
    def destruction(self) -> datetime:
        return self._destruction

    @property
    def errorSummary(self) -> str:
        return self._errorSummary

    @property
    def parameters(self) -> List[UWSParameter]:
        return self._parameters

    @property
    def results(self) -> List[UWSResult]:
        return self._results
