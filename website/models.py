from django.db import models


class Configuration(models.Model):
    """This is a model for bot configurations"""
    bot_name = models.CharField(max_length=255)
    token = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)


class TelegramChannel(models.Model):
    """This is a model for user telegram channels"""
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Tutorial(models.Model):
    """This is a model for handling the tutorials of bot """
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=2043)

class ChannelAdmin(models.Model):
    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=255)
