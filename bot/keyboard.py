from telebot import types
from bot.models import Product
from website.models import Tutorial

# Define the main keyboard
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_row1 = [types.KeyboardButton("خرید سرویس⭐️")]
buttons_row2 = [
    types.KeyboardButton("آموزش ها💡"),
    types.KeyboardButton("اشتراک های من👤"),
]
buttons_row3 = [
    types.KeyboardButton("پشتیبانی💬"),
    types.KeyboardButton("معرفی به دوستان👨‍👩‍👧‍👦"),

]
keyboard.add(*buttons_row1)
keyboard.add(*buttons_row2)
keyboard.add(*buttons_row3)

# Create inline buttons for products
product_callbacks = []
products = Product.objects.all()
inline_buttons = []
for i, product in enumerate(products, start=1):
    button_text = product.name
    callback_data = f"p_{i}"
    product_callbacks.append(callback_data)
    inline_button = types.InlineKeyboardButton(
        text=button_text, callback_data=callback_data
    )
    inline_buttons.append(inline_button)

# Create an InlineKeyboardMarkup for products
inline_keyboard_markup = types.InlineKeyboardMarkup()
for button in inline_buttons:
    inline_keyboard_markup.add(button)

# Create inline buttons for tutorials
tutorials = Tutorial.objects.all()
inline_tutorial_buttons = []
for i, tutorial in enumerate(tutorials, start=1):
    tutorial_text = tutorial.name
    telegram_id_url = tutorial.telegram_id
    inline_tutorial_button = types.InlineKeyboardButton(
        text=tutorial_text, callback_data=tutorial_text, url=telegram_id_url
    )
    inline_tutorial_buttons.append(inline_tutorial_button)

# Create an InlineKeyboardMarkup for tutorials
inline_tutorial_markup = types.InlineKeyboardMarkup()
for btn in inline_tutorial_buttons:
    inline_tutorial_markup.add(btn)

# Inline invoice confirmation keyboard
Inline_confirmation_keyboard = types.InlineKeyboardMarkup()
confirm_button = types.InlineKeyboardButton(text="تایید", callback_data="confirm")
Inline_confirmation_keyboard.add(confirm_button)

# Inline payment method keyboard
Inline_payment_keyboard = types.InlineKeyboardMarkup()
card = types.InlineKeyboardButton(text="شماره کارت", callback_data="card")
trx = types.InlineKeyboardButton(text="ارز دیجیتال ترون", callback_data="trx")
Inline_payment_keyboard.add(card, trx)

# Subscription renewal keyboard
Inline_cancel_keyboard = types.InlineKeyboardMarkup()
cancel = types.InlineKeyboardButton(text="حذف اشتراک", callback_data="cancel")
Inline_cancel_keyboard.add(cancel)
