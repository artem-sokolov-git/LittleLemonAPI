from rest_framework import serializers
from .models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")

    class Meta:
        model = MenuItem
        fields = (
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
