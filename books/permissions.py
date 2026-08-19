from rest_framework.permissions import BasePermission


class IsAdminOrListOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action == "list":
            return True

        if view.action == "retrieve":
            return request.user.is_authenticated

        return request.user.is_authenticated and request.user.is_staff
