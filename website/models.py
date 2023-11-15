from django.db import models


class ProxyCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Proxy(models.Model):
    """this isa model for proxy names in the marzban panel of the user"""
    name = models.CharField(max_length=255)
    type = models.ManyToManyField(ProxyCategory, blank=True)


class Configuration(models.Model):
    """This is a model for bot configurations"""
    panel_username = models.CharField(max_length=255, default=None)
    panel_password = models.CharField(max_length=255, default=None)
    bot_name = models.CharField(max_length=255)
    panel_url = models.CharField(max_length=255, blank=True)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.bot_name


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)

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
    """This is a model for handling the tutorials of bot """
    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=2043, default=None)

    def __str__(self):
        return self.name


class ChannelAdmin(models.Model):
    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
