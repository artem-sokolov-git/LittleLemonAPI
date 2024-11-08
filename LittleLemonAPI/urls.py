from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    MenuItemViewSet,
    OrderViewSet,
    CartViewSet,
    ManagerUserViewSet,
    DeliveryCrewViewSet,
)

router = DefaultRouter()
router.register(r"menu-items", MenuItemViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"cart/menu-items", CartViewSet)
router.register(r"groups/manager/users", ManagerUserViewSet, basename="manager")
router.register(
    r"groups/delivery-crew/users", DeliveryCrewViewSet, basename="delivery-crew"
)

urlpatterns = [
    path("", include(router.urls)),
    path("token/login/", obtain_auth_token),
]
