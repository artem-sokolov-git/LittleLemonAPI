from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token

from LittleLemonAPI.models import Category, MenuItem

restaurant_staff = (
    # ["login", "password", "group"]
    ["frankblack", "Fr@nk2007", "Admins"],
    ["alicejohnson", "Al!ce2013", "Managers"],
    ["bobbrown", "B0b!Brown23", "Managers"],
    ["edwardgreen", "Edw@rdG1reen", "Delivery_Crew"],
    ["fionablack", "F10n@BlaCk!", "Delivery_Crew"],
    ["test_user", "test_user_pass_123", None],
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
    ],
    # "Delivery_Crew": {...},
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
        # Creates a superuser if not.
        if not User.objects.filter(username="superuser").exists():
            User.objects.create_superuser(
                username="superuser",
                password="superuser123",
                email="superuser@gmail.com",
            )

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

            # creates a group if there is no such group
            if role is not None:
                group, _ = Group.objects.get_or_create(name=role)
                employee.groups.add(group)

                if role in group_permissions:
                    for codename in group_permissions[role]:
                        permission = Permission.objects.get(codename=codename)
                        group.permissions.add(permission)

            # creates tokens
            token, _ = Token.objects.get_or_create(user=employee)

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
