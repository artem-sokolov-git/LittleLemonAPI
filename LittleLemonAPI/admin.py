from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("slug", "title")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}  # Autocomplete slug field based on title


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "featured", "category")
    list_filter = ("category", "featured")
    search_fields = ("title",)
    ordering = ("title",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "menu_item", "quantity", "unit_price", "price")
    list_filter = ("user",)
    search_fields = ("user__username", "menu_item__title")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "delivery_crew", "status", "total", "date")
    list_filter = ("status", "date")
    search_fields = ("user__username",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "menu_item", "quantity", "unit_price", "price")
    list_filter = ("order",)
    search_fields = ("order__user__username", "menu_item__title")
