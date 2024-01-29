from telebot import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_row1 = [
    types.KeyboardButton('خرید سرویس⭐️'),
]
buttons_row2 = [
    types.KeyboardButton('آموزش ها💡'),
    types.KeyboardButton('اشتراک های من👤'),
]
buttons_row3 = [
    types.KeyboardButton('پشتیبانی💬')
]
keyboard.add(*buttons_row1)
keyboard.add(*buttons_row2)
keyboard.add(*buttons_row3)



