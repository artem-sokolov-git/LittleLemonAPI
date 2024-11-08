from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated


from .models import MenuItem, Cart, Order
from .serializers import (
    UserSerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
)
from .permissions import IsAdminOrManager, IsManagerOrDeliveryCrew  # noqa: F401


class ManagerUserViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminOrManager]

    def list(self, request):
        managers = User.objects.filter(groups__name="Managers")
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_id = request.data.get("id")
        username = request.data.get("username")

        if user_id:
            user = User.objects.get(id=user_id)
        if username:
            user = User.objects.get(username=username)

        group, created = Group.objects.get_or_create(name="Managers")
        if user in group.user_set.all():
            return Response(
                {"status": "User is already a Manager."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group.user_set.add(user)
        return Response(
            {"status": "User assigned to Manager"}, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk, groups__name="Managers")
        group = Group.objects.get(name="Managers")
        group.user_set.remove(user)
        return Response(
            {"status": "User removed from Manager"}, status=status.HTTP_200_OK
        )


class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsManagerOrDeliveryCrew]

    def list(self, request):
        delivery_crew = User.objects.filter(groups__name="Delivery_Crew")
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_id = request.data.get("id")
        username = request.data.get("username")

        if user_id:
            user = User.objects.get(id=user_id)
        if username:
            user = User.objects.get(username=username)

        group, created = Group.objects.get_or_create(name="Delivery_Crew")
        if user in group.user_set.all():
            return Response(
                {"status": "User is already a Delivery_Crew."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group.user_set.add(user)
        return Response(
            {"status": "User assigned to Delivery_Crew"}, status=status.HTTP_201_CREATED
        )

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk, groups__name="Delivery_Crew")
        group = Group.objects.get(name="Delivery_Crew")
        group.user_set.remove(user)
        return Response(
            {"status": "User removed from Delivery_Crew"}, status=status.HTTP_200_OK
        )


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
