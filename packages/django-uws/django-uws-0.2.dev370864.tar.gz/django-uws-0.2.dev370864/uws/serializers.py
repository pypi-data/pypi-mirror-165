from typing import List

import validators
from django.forms import ValidationError
from rest_framework import serializers

from .models import Job, JobToken, Parameter, Result

# https://www.django-rest-framework.org/api-guide/relations/


class NestedParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ["key", "value", "byReference", "isPost"]


class NestedResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ["key", "value", "size", "mimeType"]


class NestedTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobToken
        fields = ["key", "created"]


class JobSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="job-detail")
    parameters = NestedParameterSerializer(required=False, many=True)
    results = NestedResultSerializer(required=False, many=True)
    jobToken = NestedTokenSerializer(required=False, default=None)

    class Meta:
        model = Job
        fields = [
            "url",
            "jobId",
            "runId",
            "jobToken",
            "creationTime",
            "phase",
            "parameters",
            "results",
            "errorSummary",
        ]
        view_name = "job-detail"

    def create(self, validated_data: dict):
        parameter_data: List[dict] = validated_data.pop("parameters", [])
        job = Job.objects.create(**validated_data)
        # Need to create a token for the job
        JobToken.objects.create(job=job)

        for param in parameter_data:
            param.pop("isPost", None)  # remove isPost, ignore if not present

            try:
                byRef = param.get("byReference", "false") == "true"
                if byRef:
                    validators.url.validate(param.get("value"))
            except ValidationError:
                # TODO: remove incomplete job?
                raise

            Parameter.objects.create(job=job, isPost=True, **param)

        # Create empty result array on create
        job.results.set([])
        return job


class ParameterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parameter
        fields = ["url", "job", "key", "value"]


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ["url", "job", "key", "value"]
