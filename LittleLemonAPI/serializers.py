from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem, Cart


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
        fields = ["menu_item", "quantity", "price"]
        read_only_fields = ["price"]  # Автоматически рассчитывается

    def validate(self, data):
        user = self.context["request"].user
        menu_item = data.get("menu_item")  # Получаем товар из данных
        quantity = data.get("quantity")  # Получаем количество

        # Проверяем, есть ли товар уже в корзине у текущего пользователя
        cart_item = Cart.objects.filter(user=user, menu_item=menu_item).first()

        if cart_item:
            # Если товар уже есть в корзине, обновляем количество
            cart_item.quantity += quantity
            cart_item.save()
            # Возвращаем данные без необходимости создавать новый объект
            raise serializers.ValidationError("Quantity updated for existing item.")

        return data
