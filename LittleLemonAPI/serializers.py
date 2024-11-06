from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem, Cart
from django.db import IntegrityError


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
    class Meta:
        model = Cart
        fields = (
            "menu_item",
            "quantity",
            "price",
        )
        read_only_fields = ("price",)  # Automatically calculated

    def validate_menu_item(self, value):
        try:
            MenuItem.objects.get(id=value.id)
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError("This menu item does not exist")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "The price cannot be less than or equal to 0"
            )
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("The price can't be negative.")
        return value

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "This item has already been added to your cart."
            )
