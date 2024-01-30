from django.contrib import admin
from .models import Configuration, Product, TelegramChannel, Tutorial, ChannelAdmin, Message, User

admin.site.register(User)
admin.site.register(Configuration)
admin.site.register(Product)
admin.site.register(TelegramChannel)
admin.site.register(Tutorial)
admin.site.register(ChannelAdmin)
admin.site.register(Message)
