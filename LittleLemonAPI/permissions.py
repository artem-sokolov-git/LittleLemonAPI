from rest_framework import permissions


class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.groups.filter(name="Admins").exists()
                or request.user.groups.filter(name="Managers").exists()
            )
        )

class IsManagerOrDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.groups.filter(name="Managers").exists()
                or request.user.groups.filter(name="Delivery_Crew").exists()
            )
        )
