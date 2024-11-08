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
    Features:
    The path /api/groups/manager/ displays the current members of the Managers group.
    You can add a new member by going to /api/groups/manager/add/.
    You can remove a member from the group by going to /api/groups/manager/remove/id,
    where id is the user's identifier.

    Permissions:
    Only Admins and Managers have the rights to edit the data.
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
    Features:
    The path /api/groups/delivery-crew/ displays the current members of the Delivery Crew group.
    You can add a new member by going to /api/groups/delivery-crew/add/
    You can remove a member from the group by going to /api/groups/delivery-crew/remove/id
    where id is the user's identifier.

    Permissions:
    Only members of the Managers group have the rights to edit the data.
    Members of the Delivery Crew can view the list of members.
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
    """
    All users can view menu items, but only Admins and Managers can edit them.
    Items can be sorted and searched by categories.
    """

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["category__title", "title"]
    ordering_fields = ["price"]
    permission_classes = [DjangoModelPermissions]


class CartViewSet(viewsets.ModelViewSet):
    """
    Features:
    Adding an item to the cart automatically creates an order.
    Go to /api/orders to view your order.
    To clear the cart, go to /api/cart/menu-items/clear/ and click delete.

    Permissions:
    Only the customer and admin can interact with the shopping cart.
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
    Features:
    Each order has a unique order_id that can be accessed by using it as a query.
    For example: api/orders/50dfbd62-9bb5-4692-83a5-1d6b65b58e58 will bring you
    to the order page.

    Permissions:
    Managers have full rights to all orders.
    Deliverers can only interact with their own orders.
    Customers can view only their own orders.
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
