from rest_framework import permissions
from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        if not request.user.is_authenticated:
            return False

        filters: dict = {'user': request.user, 'board': obj}
        if request.method not in permissions.SAFE_METHODS:
            filters['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**filters).exists()

