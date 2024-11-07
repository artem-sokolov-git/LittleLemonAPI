from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem


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
