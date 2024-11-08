from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem, Cart, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")

    class Meta:
        model = MenuItem
        fields = (
            "id",
            "category",
            "title",
            "price",
            "featured",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "The price cannot be less than or equal to 0"
            )
        return value


class CartSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            "id",
            "menu_item",
            "title",
            "quantity",
        )

    def get_title(self, obj):
        return obj.menu_item.title if obj.menu_item else None

    def create(self, validated_data):
        user = self.context["request"].user
        order, created = Order.objects.get_or_create(
            customer=user,
            delivery_status=False,
        )
        validated_data["order"] = order
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    order_owner = serializers.CharField(source="customer.username", read_only=True)
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id",
            "order_owner",
            "items",
            "total_price",
            "created_at",
            "updated_at",
            "deliverer",
            "delivery_status",
        )

    def get_items(self, obj):
        return [f"{item.title} {item.price}" for item in obj.menu_item.all()]

    def get_total_price(self, obj):
        return sum([item.price for item in obj.menu_item.all()])

    def validate_deliverer(self, value):
        if value and not value.groups.filter(name="Delivery_Crew").exists():
            raise serializers.ValidationError(
                "The user must be in the 'Delivery' group."
            )
        return value

    def update(self, instance, validated_data):
        if "customer" in validated_data:
            instance.customer = validated_data["customer"]
        if "deliverer" in validated_data:
            instance.deliverer = validated_data["deliverer"]
        instance.delivery_status = validated_data.get(
            "delivery_status", instance.delivery_status
        )
        instance.save()
        return instance
