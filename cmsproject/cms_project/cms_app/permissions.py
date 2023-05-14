from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin users to perform write operations
    while allowing all users to have read access.
    """

    def has_permission(self, request, view):
        # Allow read access to all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write access only to admin users
        return request.user and request.user.is_staff
