"""Python Django UWS client module"""

from typing import List

import requests


class Client:
    """Python Django UWS client"""

    def __init__(self, host: str):
        """UWS Client

        Args:
            host (string): Hostname

        """

        self._host = host.rstrip("/")

    def get_job(self, job_id: int, job_token: str) -> dict:
        """Get the specified job

        Args:
            job_id (int): job identifier
            job_token (str): token used for authorization

        Returns:
            UWS Job (dict)
        """
        url = f"{self._host}/jobs/{job_id}/"
        headers = {"Authorization": f"Token {job_token}"}
        res = requests.get(url, headers=headers)
        if not res.ok:
            raise RuntimeError(res.text)

        return res.json()

    def add_results(self, job_id: int, results: List[dict], job_token: str) -> dict:
        """Add results to the specified job

        Args:
            job_id (int): job identifier
            results (List[dict]): List of a dictionaries in the format:
                {
                    "key": "res1",
                    "value": "val1",
                    "size": None|<n_bytes>,
                    "mimeType": None|str
                }
            job_token (str): token used for authorization

        Returns:
            UWS Job (dict)
        """

        # TODO: check formatting of results?
        url = f"{self._host}/jobs/{job_id}/results/"
        headers = {"Authorization": f"Token {job_token}"}
        res = requests.post(url, json=results, headers=headers)
        if not res.ok:
            raise RuntimeError(res.text)

        return res.json()

    def execute_job(self, job_id: int, job_token: str) -> dict:
        """Sets phase of the job to EXECUTING

        Args:
            job_id (int): job identifier
            job_token (str): token used for authorization

        Returns:
            UWS Job (dict)
        """
        url = f"{self._host}/jobs/{job_id}/phase/"
        headers = {"Authorization": f"Token {job_token}"}
        data = {"PHASE": "EXECUTING"}
        res = requests.post(url, data=data, headers=headers)
        if not res.ok:
            raise RuntimeError(res.text)

        return res.json()

    def complete_job(self, job_id: int, job_token: str) -> dict:
        """Sets phase of the job to COMPLETED

        NOTE: after complete, the job_token is invalidated!

        Args:
            job_id (int): job identifier
            job_token (str): token used for authorization

        Returns:
            UWS Job (dict)
        """
        url = f"{self._host}/jobs/{job_id}/phase/"
        headers = {"Authorization": f"Token {job_token}"}
        data = {"PHASE": "COMPLETE"}
        # Don't follow redirect, as the token is no longer valid
        res = requests.post(url, data=data, headers=headers, allow_redirects=False)
        if not res.ok:
            raise RuntimeError(res.text)

        return res.json()

    def fail_job(self, job_id: int, errorSummary: str, job_token: str) -> dict:
        """Sets phase of the job to ERROR and sets errorSummary

        Args:
            job_id (int): job identifier
            errorSummary (str): An error log, specifying the error
            job_token (str): token used for authorization

        Returns:
            UWS Job (dict)
        """
        headers = {"Authorization": f"Token {job_token}"}

        # errorSummary
        url = f"{self._host}/jobs/{job_id}/"
        data = {"errorSummary": errorSummary}
        res = requests.patch(url, data=data, headers=headers)
        if not res.ok:
            raise RuntimeError(res.text)

        # Phase
        data = {"PHASE": "ERROR"}
        url = f"{self._host}/jobs/{job_id}/phase/"
        # Do not follow the redirect, as the POST will invalidate the credentials
        res = requests.post(url, json=data, headers=headers, allow_redirects=False)
        if not res.ok:
            raise RuntimeError(res.text)

        return res.json()
