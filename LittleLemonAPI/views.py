from django.contrib.auth.models import User

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissions


from .models import MenuItem, Cart, Order
from .serializers import (
    ManagerSerializer,
    DeliveryCrewSerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
)
from .permissions import IsAdminOrManager, IsManagerOrDeliveryCrew, IsOwnerOrAdmin


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
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(order__customer=user)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        user = request.user
        Cart.objects.filter(order__customer=user).delete()
        return Response(
            {"success": "All items have been deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )


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
