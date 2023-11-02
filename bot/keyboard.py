from telebot import types
from website.models import Product


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_row1 = [
    types.KeyboardButton('⭐️خرید سرویس'),
]
buttons_row2 = [
    types.KeyboardButton('💬پشتیبانی'),
    types.KeyboardButton('📚راهنما اتصال'),

]
buttons_row3 = [
    types.KeyboardButton('اضافه کردن ایمیل')
]

keyboard.add(*buttons_row1)
keyboard.add(*buttons_row2)
keyboard.add(*buttons_row3)

products_keyboard = types.InlineKeyboardMarkup(row_width=1)
product_1_name = Product.objects.get(pk=1)
product_2_name = Product.objects.get(pk=2)
product_3_name = Product.objects.get(pk=3)
product_4_name = Product.objects.get(pk=4)

product_1 = types.InlineKeyboardButton(product_1_name, callback_data="product_1")
product_2 = types.InlineKeyboardButton(product_2_name, callback_data="product_2")
product_3 = types.InlineKeyboardButton(product_3_name, callback_data="product_3")
product_4 = types.InlineKeyboardButton(product_4_name, callback_data="product_4")
products_keyboard.add(product_1, product_2, product_3, product_4)
