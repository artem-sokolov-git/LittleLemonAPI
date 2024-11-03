from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import SearchFilter

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissions]


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ["category__name"]
    permission_classes = [DjangoModelPermissions]
