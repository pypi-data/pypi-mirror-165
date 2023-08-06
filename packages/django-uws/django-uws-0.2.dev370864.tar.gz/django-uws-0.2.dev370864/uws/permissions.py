"""Custom permission to support custom tokens"""

from typing import Any

from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.views import View


class RequireAuthOrOneTimeJobToken(permissions.BasePermission):
    """
    Custom permission to only allow Authenticated user to access job
    And tokens only for specific jobs
    """

    def has_permission(self, request: HttpRequest, view: View):
        if "Authorization" in request.headers:
            return True  # Token content will be checked later in the object permission

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any):
        # Require a one time token specified in the Authorization header
        if "Authorization" in request.headers:
            auth_data = request.headers["Authorization"].split()
            if len(auth_data) == 2 and auth_data[0] == "Token" and auth_data[1] != "":
                # Compare the values of the job's token and the one supplied
                # in the header.
                key = getattr(obj.token, "key", None)
                return key == auth_data[1]

        # Always allow authenticated users
        return bool(request.user and request.user.is_authenticated)
