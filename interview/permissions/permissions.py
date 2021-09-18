from rest_framework.permissions import BasePermission


class PostOnlyPermissions(BasePermission):
    def has_permission(self, request, view):
        print(dir(request))
        print(dir(view))
        return False