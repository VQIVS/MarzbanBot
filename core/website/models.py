from datetime import timezone
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.conf import settings


class Configuration(models.Model):
    """This is a model for bot configurations"""

    panel_username = models.CharField(max_length=255, default=None)
    panel_password = models.CharField(max_length=255, default=None)
    bot_name = models.CharField(max_length=255)
    bot_url = models.CharField(max_length=255, default=None, blank=True)
    panel_url = models.CharField(max_length=255, blank=True)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.bot_name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=0, max_digits=10)
    data_limit = models.IntegerField()
    expire = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class TelegramChannel(models.Model):
    """This is a model for user telegram channels"""

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tutorial(models.Model):
    """This is a model for handling the tutorials of bot"""

    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=2043, default=None)

    def __str__(self):
        return self.name


class ChannelAdmin(models.Model):
    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.subject


class PaymentMethod(models.Model):
    holders_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.holders_name


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="bot/payment_photos/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} made at {self.timestamp}"


class MajorProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    data_limit = models.IntegerField(default=0)
    expire = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    code = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    active = models.BooleanField(default=True)
    discount_percent = models.FloatField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    use_limit = models.IntegerField(default=1)
    times_used = models.IntegerField(default=0)

    def __str__(self):
        return self.code

    def is_valid(self):
        """ Check if the code is still active, within the valid date range, and under the use limit. """
        if not self.active:
            return False
        if self.times_used >= self.use_limit:
            return False
        if not (self.valid_from <= timezone.now() <= self.valid_to):
            return False
        return True

    def use(self):
        """ Increment the usage count of the code. """
        if self.is_valid():
            self.times_used += 1
            self.save()
            return True
        return False


# class ForceChannel(models.Model):
#     channel_id = models.CharField(max_length=255)
#     channel_username = models.CharField(max_length=255)

#     def __str__(self):
#         return f"Telegram Channel ID: {self.channel_id})"
