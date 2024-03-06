from django.db import models


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
    price = models.DecimalField(max_digits=10, decimal_places=0)
    data_limit = models.FloatField()
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
