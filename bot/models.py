from django.db import models

from website.models import Product

"""Models for first version"""

# class Email(models.Model):
#     address = models.EmailField(max_length=255, unique=True)
#
#     def __str__(self):
#         return self.address
#
#
# class User(models.Model):
#     """A class for User objects"""
#     user_id = models.IntegerField()
#     primary_email = models.EmailField(max_length=255)
#     emails = models.ManyToManyField('Email', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.user_id)
#
#
# class Order(models.Model):
#     """"A class for Order objects"""
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_by_user")
#     email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name="orders_by_email")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     status = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.email


""" Models for version 2.00 """


class BotUser(models.Model):
    """A class for User objects"""

    user_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id)


class Subscription(models.Model):
    """A class to handle the subscriptions"""

    user_id = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    sub_user = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id)


class Order(models.Model):
    """"A class for Order objects"""

    user_id = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    status = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_id)

