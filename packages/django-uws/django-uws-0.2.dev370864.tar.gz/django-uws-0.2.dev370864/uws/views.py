from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action

import uws.tasks
from uws.models import EXECUTION_PHASES, Job
from uws.serializers import JobSerializer, ResultSerializer

from .permissions import RequireAuthOrOneTimeJobToken


def queue_job(job: Job) -> Job:
    """Set a queued phase and dispatches it to the queue"""
    job.phase = EXECUTION_PHASES.QUEUED
    job.save()

    uws.tasks.start_job.delay(job_id=job.pk, job_token=job.token.key)

    return job


def execute_job(job: Job) -> Job:
    """Sets the phase to executing"""
    job.phase = EXECUTION_PHASES.EXECUTING
    job.startTime = datetime.now()
    job.save()

    return job


def _finalize_job(job: Job) -> Job:
    job.endTime = datetime.now()
    job.jobToken.delete()
    job.save()

    return job


def error_job(job: Job) -> Job:
    """Sets the phase to error"""
    job.phase = EXECUTION_PHASES.ERROR
    return _finalize_job(job)


def abort_job(job: Job) -> Job:
    """Aborts the job and dispatches it to the queue"""
    job.phase = EXECUTION_PHASES.ABORTED
    # TODO: Try abort job from Celery
    return _finalize_job(job)


def complete_job(job: Job) -> Job:
    """Complete a job"""
    job.phase = EXECUTION_PHASES.COMPLETED
    return _finalize_job(job)


# Command Mapping (switch statement)
COMMANDS = {
    "RUN": queue_job,
    "EXECUTING": execute_job,
    "ABORT": abort_job,
    "COMPLETE": complete_job,
    "ERROR": error_job,
}


class JobModelViewSet(viewsets.ModelViewSet):
    """DRF ModelViewSet for UWS Jobs"""

    queryset = Job.objects.all().order_by("-creationTime")
    serializer_class = JobSerializer
    permission_classes = [RequireAuthOrOneTimeJobToken]

    def create(self, request: HttpRequest, *args, **kwargs):
        # Update status_code following the UWS REST spec
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_303_SEE_OTHER
        return response

    def destroy(self, request: HttpRequest, *args, **kwargs):
        # TODO: perform abort etc.
        return self.destroy(request, *args, **kwargs)

    @action(
        detail=True, methods=["post"], permission_classes=[RequireAuthOrOneTimeJobToken]
    )
    def phase(self, request: HttpRequest, pk: int = None) -> HttpResponse:

        # performs the check_object_permission for token auth
        job: Job = self.get_object()

        requested_phase = request.data["PHASE"]
        if requested_phase not in COMMANDS:
            data = {"detail": "invalid phase"}
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Check for valid phase transitions (e.g. COMPLETED can not be RUN)

        job = COMMANDS[requested_phase](job)

        serializer = JobSerializer(job, context={"request": request})
        headers = {"Location": reverse("job-detail", kwargs={"pk": job.pk})}

        return JsonResponse(
            data=serializer.data, status=status.HTTP_303_SEE_OTHER, headers=headers
        )

    @action(
        detail=True, methods=["post"], permission_classes=[RequireAuthOrOneTimeJobToken]
    )
    def results(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        # performs the check_object_permission for token auth
        job: Job = self.get_object()
        serialized_job = JobSerializer(job, context={"request": request})

        url = serialized_job.data["url"]

        # Support posting a list of results
        data = request.data
        is_list = isinstance(request.data, list)
        if is_list:
            data = list(map(lambda x: {**x, "job": url}, data))
        else:
            data["job"] = job  # Add job

        result = ResultSerializer(data=data, context={"request": request}, many=is_list)

        # Create results
        if result.is_valid():
            result.save()
        else:
            return JsonResponse(
                data={"detail": "invalid job result"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Need to fetch the new data with results
        job.refresh_from_db()
        serialized_job = JobSerializer(job, context={"request": request})

        return JsonResponse(
            data=serialized_job.data,
            status=status.HTTP_201_CREATED,
        )
