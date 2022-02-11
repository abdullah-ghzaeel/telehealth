from rest_framework.permissions import BasePermission
from doctor.models import Doctor


class IsDoctor(BasePermission):
    """
    Allows access only to doctor users.
    """

    def has_permission(self, request, view):
        return bool(request.user and Doctor.objects.filter(user=request.user).exists())
