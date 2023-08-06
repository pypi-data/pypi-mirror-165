""" Abstract Worker class """

from abc import ABCMeta, abstractmethod

from uws.classes import UWSJob
from uws.client import Client


class Worker(metaclass=ABCMeta):
    """Abstract Worker class"""

    def __init__(self):
        self._type = None

    @abstractmethod
    def run(self, job: UWSJob, job_token: str, client: Client) -> None:
        pass

    @property
    def type(self):
        return self._type
