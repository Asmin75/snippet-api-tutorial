from rest_framework import permissions


# class IsOwnerOrReadonly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.owner == request.user


class IsAllowedToWrite(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "User"


class IsAllowedToRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        if view.action == ['create', 'retrieve', 'update', 'destroy']:
            return request.user.user_type == "User" or request.user.user_type == "Admin"
    def has_object_permission(self, request, view, obj):
        return obj.is_allowed_to_read == "YES"