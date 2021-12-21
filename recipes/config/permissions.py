from rest_framework.permissions import BasePermission, SAFE_METHODS


# TODO - Implement permissions for user follower read only.

# class IsStaff(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_staff

# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS
