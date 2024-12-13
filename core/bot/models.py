import uuid

from django.db import models
from website.models import MajorProduct, Product


class BotUser(models.Model):
    """
    Represents a bot user.
    """

    user_id = models.IntegerField(unique=True)
    test_status = models.CharField(max_length=250, blank=True, null=True)
    is_banned = models.BooleanField(default=False)
    status = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    selected_product_id = models.IntegerField(null=True, blank=True)
    invited_by = models.IntegerField(null=True, blank=True)
    has_received_prize = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id)


class Subscription(models.Model):
    """A class to handle the subscriptions"""

    user_id = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    sub_user = models.CharField(max_length=255)
    status = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    """A class for Order objects"""

    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True
    )
    order_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    major_product = models.ForeignKey(
        MajorProduct, on_delete=models.CASCADE, blank=True, null=True
    )
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Order {self.order_id} for {self.user} ({self.product})"
            if self.product
            else f"Order {self.order_id} for {self.user} (No product)"
        )
