from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwner(permissions.BasePermission):
    """
    Allows access only to creator of object.
    """
    message = "Bu amalni faqat ob`ekt yaratuvchisi bajara oladi"

    def has_object_permission(self, request, view, obj):
        # Allows to creator of book.
        if obj.profile.user != request.user:
            raise PermissionDenied(detail="Siz faqat o`zingiz yaratgan kitobni o`zgartira olasiz.")
        return True
