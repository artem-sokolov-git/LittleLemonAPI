from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from LittleLemonAPI.models import Category, MenuItem  # noqa: W291

restaurant_staff = (
    # ["login", "password", "group"]
    ["frankblack", "p#LFe#sVEdxT3Lx", "Admins"],
    ["alicejohnson", "7iF54Hq#ub7nP8b", "Managers"],
    ["bobbrown", "rc3i.X3brxXZnbg", "Managers"],
    ["edwardgreen", ".aTc3#ti.ed86QK", "Deliverers"],
    ["fionablack", "!!L2M!CEEgm#zi7", "Deliverers"],
)

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
                defaults={"password": password, "email": f"{login}@gmail.com"},
            )
            if created:
                # creates a group if there is no such group
                group, _ = Group.objects.get_or_create(name=role)
                # adds the employee to the appropriate group
                employee.groups.add(group)

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
