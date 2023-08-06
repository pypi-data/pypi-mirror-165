import binascii
import os

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _


class EXECUTION_PHASES(models.TextChoices):
    """UWS Execution phases

    See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#ExecutionPhase
    """

    PENDING = "PENDING", _("pending")
    QUEUED = "QUEUED", _("queued")
    EXECUTING = "EXECUTING", _("executing")
    COMPLETED = "COMPLETED", _("completed")
    ERROR = "ERROR", _("error")
    ABORTED = "ABORTED", _("aborted")
    UNKNOWN = "UNKNOWN", _("unknown")
    HELD = "HELD", _("held")
    SUSPENDED = "SUSPENDED", _("suspended")
    ARCHIVED = "ARCHIVED", _("archived")


class Job(models.Model):
    """UWS Job"""

    jobId = models.BigAutoField(
        verbose_name=_("job identifier"),
        name="jobId",
        help_text="Primary identifier",
        primary_key=True,
    )

    runId = models.CharField(
        verbose_name=_("client supplied identifier"),
        name="runId",
        max_length=128,
        help_text="See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#runId",
    )

    ownerId = models.CharField(
        verbose_name=_("owner id of the job"),
        name="ownerId",
        max_length=64,
        null=True,
        blank=True,
        help_text="See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#ownerId",
    )

    phase = models.CharField(
        verbose_name=_("execution phase"),
        name="phase",
        max_length=16,
        choices=EXECUTION_PHASES.choices,
        default="PENDING",
        help_text="See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#ExecutionPhase",
    )

    quote = models.DateTimeField(
        verbose_name=_("predicted end time"),
        name="quote",
        null=True,
        blank=True,
        help_text="See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#Quote",
    )

    creationTime = models.DateTimeField(
        verbose_name=_("job creation time"),
        name="creationTime",
        auto_now_add=True,
        help_text="DateTime when job was created",
    )

    startTime = models.DateTimeField(
        verbose_name=_("job execution start time"),
        name="startTime",
        null=True,
        blank=True,
    )

    endTime = models.DateTimeField(
        verbose_name=_("job execution finished time"),
        name="endTime",
        null=True,
        blank=True,
    )

    executionDuration = models.IntegerField(
        verbose_name=_("execution duration in seconds"),
        name="executionDuration",
        default=0,
        help_text="Time limit after which the job will be aborted, 0 for no limit",
    )

    destruction = models.DateTimeField(
        verbose_name=_("job destruction time"),
        name="destruction",
        null=True,
        blank=True,
        help_text="See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#DestructionTime",
    )

    errorSummary = models.TextField(
        verbose_name=_("job error summary"),
        name="errorSummary",
        null=True,
        blank=True,
        help_text="See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#Error",
    )

    @property
    def token(self):
        try:
            return self.jobToken
        except ObjectDoesNotExist:
            return None

    class Meta:
        ordering = ["creationTime"]
        verbose_name = _("job")
        verbose_name_plural = _("jobs")
        app_label = "uws"


class Parameter(models.Model):
    """UWS Job Parameters

    See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#ResultsList2
    """

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="parameters",
        related_query_name="parameter",
    )

    key = models.CharField(
        verbose_name=_("paramater key"),
        name="key",
        max_length=64,
        help_text="Paramater key",
    )

    value = models.TextField(verbose_name=_("paramater value"), name="value")

    byReference = models.BooleanField(
        verbose_name=_("is a reference"), name="byReference", default=False
    )

    isPost = models.BooleanField(
        verbose_name=_("is posted"), name="isPost", default=False
    )

    class Meta:
        unique_together = ("job", "key")
        verbose_name = _("parameter")
        verbose_name_plural = _("parameters")
        app_label = "uws"


class Result(models.Model):
    """UWS Job Result

    See https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html#ResultsList
    """

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="results",
        related_query_name="result",
    )

    key = models.CharField(
        verbose_name=_("paramater key"),
        name="key",
        max_length=64,
        help_text="Paramater key",
    )

    value = models.TextField(
        verbose_name=_("paramater value"),
        name="value",
        help_text="Usually a reference URI to a resource",
    )

    size = models.BigIntegerField(
        verbose_name=_("resource size"), name="size", null=True, blank=True
    )

    mimeType = models.CharField(
        verbose_name="result mime-type",
        name="mimeType",
        max_length=128,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("job", "key")
        verbose_name = _("result")
        verbose_name_plural = _("results")
        app_label = "uws"


class JobToken(models.Model):
    """
    Job one-time authorization token model.
    """

    key = models.CharField(
        verbose_name=_("key"), name="key", max_length=40, primary_key=True
    )
    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="jobToken",
        verbose_name=_("job"),
    )
    created = models.DateTimeField(
        verbose_name=_("Created"), name="created", auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        # This method has been copied from: https://github.com/encode/django-rest-framework/blob/b25ac6c5e36403f62b13163a0190eaa48b586c47/rest_framework/authtoken/models.py#L37
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("jobtoken")
        verbose_name_plural = _("jobtokens")
        app_label = "uws"
