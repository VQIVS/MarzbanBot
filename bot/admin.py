from django.contrib import admin
from .models import BotUser, Order, Subscription

admin.site.register(BotUser)
admin.site.register(Order)
admin.site.register(Subscription)
