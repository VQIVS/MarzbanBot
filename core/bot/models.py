from django.db import models
from website.models import Product, MajorProduct
import uuid


class BotUser(models.Model):
    """
    Represents a bot user.
    """

    user_id = models.IntegerField(unique=True)
    test_status = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    selected_product_id = models.IntegerField(null=True, blank=True)
    invited_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    invited_user = models.ManyToManyField('self', blank=True)
    has_received_prize = models.BooleanField(default=False)
    point = models.IntegerField(null=True, blank=True)
    total_sub_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_sub_user(self):
        """
        Update the total_sub_count field with the count of existing subscriptions.
        """
        self.total_sub_count = Subscription.objects.filter(user_id=self).count()
        self.save()

    def __str__(self):
        return str(self.user_id)


class Subscription(models.Model):
    """A class to handle the subscriptions"""

    user_id = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    sub_user = models.CharField(max_length=255)
    status = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id)


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
