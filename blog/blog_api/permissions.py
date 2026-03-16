from rest_framework import permissions

class IsOwnerOrReadOnlyObject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        return obj.user == request.user

class ArticlePermission(BaseException):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=("User", "Moderator")).exists()

        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user.groups.filter(name="Moderator").exists()

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=("User", "Moderator")).exists()

        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user.groups.filter(name="Moderator").exists()

        return False