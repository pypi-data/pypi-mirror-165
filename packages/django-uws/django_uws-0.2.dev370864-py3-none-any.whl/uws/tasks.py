import traceback
from typing import Dict

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from uws.classes import UWSJob
from uws.client import Client
from uws.workers import Worker

logger = get_task_logger(__name__)


# TODO: think about what to do on worker defining the same type
def init_workers() -> Dict[str, Worker]:
    tmp = {}

    for worker_name in getattr(settings, "UWS_WORKERS", []):
        worker: Worker = import_string(worker_name)()
        tmp[worker.type] = worker

    # TODO: Remove reference to ESAP_WORKERS, kept here for legacy reasons
    for worker_name in getattr(settings, "ESAP_WORKERS", []):
        worker: Worker = import_string(worker_name)()
        tmp[worker.type] = worker

    if len(tmp.keys()) == 0:
        logger.warning("No worker implementations configured!")

    return tmp


REGISTERED_WORKERS = init_workers()


@shared_task
def start_job(job_id: int, job_token: str):
    logger.info("Start processing for job %i", job_id)

    host = getattr(settings, "UWS_HOST", None)
    if host is None:
        raise ImproperlyConfigured(f"Invalid `UWS_HOST` setting: `{host}`")
    client = Client(host)

    try:
        job = UWSJob(client.get_job(job_id, job_token))
    except Exception as err:
        # In case an issue is found with retrieving the job
        # fail the celery job, so a retry can be attempted
        logger.exception(err)
        raise err

    try:
        parameters = {}
        for param in job.parameters:
            parameters[param.key] = param.value

        logger.debug("Job parameters: %s", parameters)

        # Determine which worker to run
        worker_type = parameters["type"]
        if worker_type not in REGISTERED_WORKERS:
            raise RuntimeError(f"Unknown worker type: `{worker_type}`")
        worker = REGISTERED_WORKERS[worker_type]

        # Mark it started
        client.execute_job(job_id, job_token=job_token)

        worker.run(job, job_token, client)

        client.complete_job(job_id, job_token)
    except Exception as err:
        logger.exception(err)
        # Store log in job log
        trace_back = "".join(traceback.format_exception(err))
        client.fail_job(job_id, trace_back, job_token)

        # The celery job finished successfully, however the UWS job did not.
        # It should not be retried automatically
