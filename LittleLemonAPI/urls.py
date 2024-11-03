from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import MenuItemViewSet

router = DefaultRouter()
router.register(r"menu-items", MenuItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/login/", obtain_auth_token),
]
