from django.db import models
from django.contrib.auth.models import User  # noqa: F401


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def price(self):
        return self.quantity * self.menu_item.price

    @staticmethod
    def get_total_price(user):
        cart_items = Cart.objects.filter(user=user)
        return sum(item.price for item in cart_items)

    class Meta:
        # unique_together = ("menu_item", "user")
        constraints = [
            models.UniqueConstraint(fields=["menu_item", "user"], name="user_item")
        ]


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     delivery_crew = models.ForeignKey(
#         User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True
#     )
#     status = models.BooleanField(db_index=True, default=False)
#     total = models.DecimalField(max_digits=6, decimal_places=2)
#     date = models.DateField(db_index=True)


# class OrderItem(models.Model):
#     order = models.ForeignKey(
#         Order, on_delete=models.CASCADE
#     )  # there should be a binding to the Order model here.
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     quantity = models.SmallIntegerField()
#     unit_price = models.DecimalField(max_digits=6, decimal_places=2)
#     price = models.DecimalField(max_digits=6, decimal_places=2)

#     class Meta:
#         unique_together = ("order", "menu_item")
