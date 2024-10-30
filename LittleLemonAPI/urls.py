from django.urls import path
from .views import MenuItemViewSet

urlpatterns = [
    path("menu-items/", MenuItemViewSet.as_view({"get": "list"}), name="menu-items"),
]
