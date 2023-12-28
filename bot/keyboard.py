from telebot import types
from website.models import Product, Tutorial

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_row1 = [
    types.KeyboardButton('⭐️خرید سرویس'),
]
buttons_row2 = [
    types.KeyboardButton('💬پشتیبانی'),
    types.KeyboardButton('📚راهنما اتصال'),
    types.KeyboardButton('اضافه کردن ایمیل')
]
buttons_row3 = [
    types.KeyboardButton('اشتراک های من')
]
keyboard.add(*buttons_row1)
keyboard.add(*buttons_row2)
keyboard.add(*buttons_row3)


products_keyboard = types.InlineKeyboardMarkup(row_width=1)
product_1_name = Product.objects.get(pk=1)
product_2_name = Product.objects.get(pk=2)
product_3_name = Product.objects.get(pk=3)
product_4_name = Product.objects.get(pk=4)

product_1 = types.InlineKeyboardButton(product_1_name.name, callback_data=product_1_name.id)
product_2 = types.InlineKeyboardButton(product_2_name.name, callback_data=product_2_name.id)
product_3 = types.InlineKeyboardButton(product_3_name.name, callback_data=product_3_name.id)
product_4 = types.InlineKeyboardButton(product_4_name.name, callback_data=product_4_name.id)
products_keyboard.add(product_1, product_2, product_3, product_4)

tutorial = Tutorial.objects.get(pk=1)
channel_id = types.InlineKeyboardButton("آموزش ها", callback_data="tt", url=tutorial.telegram_id)
tutorial_keyboard = types.InlineKeyboardMarkup(row_width=1)
tutorial_keyboard.add(channel_id)
