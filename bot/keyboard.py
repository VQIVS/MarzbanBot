from telebot import types
from bot.models import Product

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

products = Product.objects.all()

# Create a list of inline buttons
inline_buttons = []
for i, product in enumerate(products, start=1):

    button_text = product.name
    callback_data = f"p_{i}"
    inline_button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
    inline_buttons.append(inline_button)

inline_keyboard_markup = types.InlineKeyboardMarkup()
for button in inline_buttons:
    inline_keyboard_markup.add(button)

