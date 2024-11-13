from rest_framework import permissions


class IsAdminOrManagerOrDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.groups.filter(name="Admins").exists()
                or request.user.groups.filter(name="Managers").exists()
                or request.user.groups.filter(name="Delivery_Crew").exists()
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


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.user.groups.filter(name="Admins").exists()
            or obj.order.customer == request.user
        ):
            return True
        else:
            return False
