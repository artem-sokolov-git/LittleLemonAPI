from rest_framework import serializers
from .models import Category, MenuItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title",)


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = (
            "title",
            "price",
            "featured",
            "category",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "The price cannot be less than or equal to 0"
            )
        return value
