import uuid
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(
        User, related_name="customer_orders", on_delete=models.CASCADE
    )
    deliverer = models.ForeignKey(
        User,
        related_name="deliverer_orders",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    delivery_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    menu_item = models.ManyToManyField(MenuItem, through="Cart", related_name="orders")


class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_subtotal(self):
        return self.menu_item.price * self.quantity
