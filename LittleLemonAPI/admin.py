from django.contrib import admin
from .models import Category, MenuItem, Order, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "featured", "category")
    list_filter = ("featured", "category")
    search_fields = ("title",)
    ordering = ("title",)
    autocomplete_fields = ("category",)  # Удобно, если категорий много


class CartInline(admin.TabularInline):
    model = Cart
    extra = 1
    readonly_fields = ("item_subtotal",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "customer",
        "deliverer",
        "delivery_status",
        "created_at",
    )
    list_filter = ("delivery_status", "created_at", "updated_at")
    search_fields = ("order_id", "customer__username", "deliverer__username")
    date_hierarchy = "created_at"
    inlines = [CartInline]
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("order__customer", "menu_item", "quantity", "item_subtotal")
    list_filter = ("order", "menu_item")
    search_fields = ("order__order_id", "menu_item__title")
    readonly_fields = ("item_subtotal",)
