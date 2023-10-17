from django.contrib import admin
from .models import Email, User, Order

admin.site.register(Email)
admin.site.register(User)
admin.site.register(Order)