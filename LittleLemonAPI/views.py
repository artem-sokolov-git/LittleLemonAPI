from django.contrib.auth.models import User, Group

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissions


from .models import MenuItem, Cart, Order
from .serializers import (
    UserSerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
)
from .permissions import (
    IsAdminOrManagerOrDeliveryCrew,
    IsManagerOrDeliveryCrew,
    IsOwnerOrAdmin,
)


class ManagerViewSet(viewsets.ModelViewSet):
    """
    Available actions:
    -------------------------------------
    * GET /api/groups/manager/
    --------------------------------------
    * GET /api/groups/manager/add/
    --------------------------------------
    * POST /api/groups/manager/add/
    --------------------------------------
    * DELETE /api/groups/manager/remove/<id>
    -------------------------------------
    Access Rights:
        Only managers and the delivery team have access to this ViewSet.
    """

    queryset = User.objects.filter(groups__name="Managers")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrManagerOrDeliveryCrew]

    @action(detail=False, methods=["post", "get"], url_path="add")
    def add_manager(self, request):
        if request.method == "GET":
            non_managers = User.objects.exclude(groups__name="Managers")
            serializer = self.get_serializer(non_managers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            username = request.data.get("username")
            user = User.objects.get(username=username)
            manager_group, created = Group.objects.get_or_create(name="Managers")
            if not user.groups.filter(name="Managers").exists():
                user.groups.add(manager_group)
                user.save()
                return Response(
                    {"detail": "User assigned to Managers group."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"detail": "User is already a member of the Managers group."},
                    status=status.HTTP_200_OK,
                )

    @action(detail=False, methods=["delete"], url_path="remove/(?P<id>[0-9]+)")
    def remove_manager(self, request, id=None):
        user = User.objects.get(pk=id)
        if user.groups.filter(name="Managers").exists():
            user.groups.remove(Group.objects.get(name="Managers"))
            user.save()
            return Response(
                {"detail": "User removed from Managers group."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "User is not a member of the Managers group."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeliveryCrewViewSet(viewsets.ModelViewSet):
    """
    Available actions:
    -------------------------------------
    * GET /api/groups/delivery-crew/
    --------------------------------------
    * GET /api/groups/delivery-crew/add/
    --------------------------------------
    * POST /api/groups/delivery-crew/add/
    --------------------------------------
    * DELETE /api/groups/delivery-crew/remove/<id>
    -------------------------------------
    Access Rights:
        Only managers and the delivery team have access to this ViewSet.
    """

    queryset = User.objects.filter(groups__name="Delivery_Crew")
    serializer_class = UserSerializer
    permission_classes = [IsManagerOrDeliveryCrew]

    @action(detail=False, methods=["post", "get"], url_path="add")
    def add_deliverer(self, request):
        if request.method == "GET":
            non_deliverer = User.objects.exclude(groups__name="Delivery_Crew")
            serializer = self.get_serializer(non_deliverer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            username = request.data.get("username")
            user = User.objects.get(username=username)
            delivery_group, created = Group.objects.get_or_create(name="Delivery_Crew")
            if not user.groups.filter(name="Delivery_Crew").exists():
                user.groups.add(delivery_group)
                user.save()
                return Response(
                    {"detail": "User assigned to Delivery_Crew."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"detail": "User is already a member of the Delivery_Crew."},
                    status=status.HTTP_200_OK,
                )

    @action(detail=False, methods=["delete"], url_path="remove/(?P<id>[0-9]+)")
    def remove_deliverer(self, request, id=None):
        user = User.objects.get(pk=id)
        if user.groups.filter(name="Delivery_Crew").exists():
            user.groups.remove(Group.objects.get(name="Delivery_Crew"))
            user.save()
            return Response(
                {"detail": "User removed from Delivery_Crew."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "User is not a member of the Delivery_Crew."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["category__title", "title"]
    ordering_fields = ["price"]
    permission_classes = [DjangoModelPermissions]


class CartViewSet(viewsets.ModelViewSet):
    """
    Adding an item to the cart automatically creates an order.
    Only the customer and admin can interact with the shopping cart.
    Go to /api/orders to view your order.
    To clear the cart go to /api/cart/menu-items/clear/ and click delete.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(order__customer=user)

    @action(detail=False, methods=["delete"], url_path="clear")
    def clear_cart(self, request):
        user = request.user
        Cart.objects.filter(order__customer=user).delete()
        return Response(
            {"success": "All items have been deleted!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class OrderViewSet(viewsets.ModelViewSet):
    """
    Особенности:
    Каждый Order имеет уникальный order_id на который можно перейти указав его как query
    Например: api/orders/50dfbd62-9bb5-4692-83a5-1d6b65b58e58 перенесет вас на страницу
    заказа.

    Права:
    Менеджеры имеют полные права для всех заказов
    Deliverer может взаимодействовать только со своим заказом
    Customers могут просматривать только свои заказы
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Managers"):
            return Order.objects.all()
        if user.groups.filter(name="Delivery_Crew"):
            return Order.objects.filter(deliverer=user.id)
        else:
            return Order.objects.filter(customer=user)
