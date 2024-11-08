from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated


from .models import MenuItem, Cart, Order
from .serializers import (
    ManagerSerializer,
    DeliveryCrewSerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
)
from .permissions import IsAdminOrManager, IsManagerOrDeliveryCrew


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name="Managers")
    serializer_class = ManagerSerializer
    permission_classes = [IsAdminOrManager]


class DeliveryCrewViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name="Delivery_Crew")
    serializer_class = DeliveryCrewSerializer
    permission_classes = [IsManagerOrDeliveryCrew]


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["category__title", "title"]
    ordering_fields = ["price"]
    permission_classes = [DjangoModelPermissions]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Cart.objects.all()
        else:
            return Cart.objects.filter(order__customer=user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=user)
