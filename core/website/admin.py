from django.contrib import admin

from .models import (
    ChannelAdmin,
    Configuration,
    DiscountCode,
    MajorProduct,
    Message,
    Payment,
    PaymentMethod,
    Product,
    TelegramChannel,
    Tutorial,
)

admin.site.register(Configuration)
admin.site.register(Product)
admin.site.register(TelegramChannel)
admin.site.register(Tutorial)
admin.site.register(ChannelAdmin)
admin.site.register(Message)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(MajorProduct)
admin.site.register(DiscountCode)
