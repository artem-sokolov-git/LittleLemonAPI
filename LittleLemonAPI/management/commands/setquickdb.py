import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

from LittleLemonAPI.models import Category, MenuItem, Order, Cart

restaurant_staff = (
    # ["login", "password", "group"]
    ["admin_frank", "Fr@nk2007", "Admins"],
    ["manager_alice", "Al!ce2013", "Managers"],
    ["manager_bob", "B0b!Brown23", "Managers"],
    ["deliverer_edward", "Edw@rdG1reen", "Delivery_Crew"],
    ["deliverer_fiona", "F10n@BlaCk!", "Delivery_Crew"],
)

customers = (
    ["customer_linda", "linda_123"],
    ["customer_franklin", "franklin_123"],
    ["customer_sara", "sara_123"],
)

group_permissions = {
    "Admins": [
        "add_category",
        "add_menuitem",
        "change_category",
        "change_menuitem",
        "add_user",
        "change_user",
    ],
    "Managers": [
        "add_category",
        "add_menuitem",
        "change_category",
        "change_menuitem",
        "view_order",
        "change_order",
        "delete_order",
    ],
    "Delivery_Crew": [
        "view_order",
        "change_order",
    ],
}

menu_items = (
    # ["title", "price", "category"]
    ["Bruschetta", 6.50, "Appetizers"],
    ["Caesar Salad", 9.00, "Salads"],
    ["Margherita Pizza", 12.00, "Main Course"],
    ["Spaghetti Carbonara", 14.00, "Main Course"],
    ["Grilled Ribeye Steak", 25.00, "Main Course"],
    ["Lobster Bisque", 11.50, "Soups"],
    ["Tiramisu", 7.00, "Desserts"],
    ["Cheesecake", 6.50, "Desserts"],
    ["Espresso", 3.00, "Beverages"],
    ["Red Wine Glass", 8.00, "Beverages"],
)


class Command(BaseCommand):
    help = """Creates superuser, admin groups, managers, delivery people,
    menu item database with categories."""

    def handle(self, *args, **kwargs):
        ### CREATE SUPERSUER
        if not User.objects.filter(username="superuser").exists():
            User.objects.create_superuser(
                username="superuser",
                password="superuser123",
                email="superuser@email.com",
            )

        ### CREATE CATEGORIES AND MENU_ITEMS
        for title, price, category in menu_items:
            category_obj, _ = Category.objects.get_or_create(
                title=category, slug=category.lower().replace(" ", "-")
            )
            item, _ = MenuItem.objects.get_or_create(
                title=title,
                defaults={
                    "price": price,
                    "featured": False,
                    "category": category_obj,
                },
            )

        ### CREATE RESTAURANT_STAFF
        for login, password, role in restaurant_staff:
            # Creates an employee if not.
            employee, created = User.objects.get_or_create(
                username=login,
                defaults={
                    "password": password,
                    "email": f"{login}@email.com",
                    "is_staff": True,
                },
            )

            if created:
                employee.set_password(password)
                employee.save()

            group, _ = Group.objects.get_or_create(name=role)
            employee.groups.add(group)

            if role in group_permissions:
                for codename in group_permissions[role]:
                    permission = Permission.objects.get(codename=codename)
                    group.permissions.add(permission)

            # creates tokens
            token, _ = Token.objects.get_or_create(user=employee)

        ### CREATE CUSTOMERS
        for login, password in customers:
            customer, created = User.objects.get_or_create(
                username=login,
                defaults={
                    "password": password,
                    "email": f"{login}@email.com",
                },
            )

            if created:
                customer.set_password(password)
                customer.save()

            token, _ = Token.objects.get_or_create(user=customer)

            order = Order.objects.create(customer=customer)
            for item_data in random.sample(list(menu_items), 2):
                title, price, category = item_data
                menu_item = MenuItem.objects.get(title=title)
                Cart.objects.create(
                    order=order, menu_item=menu_item, quantity=random.randint(1, 3)
                )
