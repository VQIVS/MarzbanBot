from telebot import TeleBot
from website.models import Configuration, Message, ChannelAdmin, Product
from bot.models import BotUser
import os
import django
from bot.keyboard import keyboard, inline_keyboard_markup, inline_tutorial_markup, product_callbacks, Inline_confirmation_keyboard
from django.db import IntegrityError

""" get the needle data from db """
configuration = Configuration.objects.first()
message_bot = Message.objects.first()
token = configuration.token
bot = TeleBot(token)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


@bot.message_handler(['start'])
def start(message):
    user_id = message.from_user.id

    try:
        bot_user = BotUser(user_id=user_id)
        bot_user.save()
    except IntegrityError:
        pass

    text = message_bot.text
    bot.send_message(user_id, text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'آموزش ها💡')
def handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "لطفا سیستم عامل خود را انتخاب کنید", reply_markup=inline_tutorial_markup)


@bot.message_handler(func=lambda message: message.text == 'پشتیبانی💬')
def handler(message):
    user_id = message.from_user.id
    support_admin = ChannelAdmin.objects.values('telegram_id').first()['telegram_id']
    bot.send_message(user_id, support_admin)


@bot.message_handler(func=lambda message: message.text == 'خرید سرویس⭐️')
def handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "message", reply_markup=inline_keyboard_markup)


@bot.callback_query_handler(func=lambda query: query.data.startswith('p_'))
def create_invoice(query):
    user_id = query.message.chat.id
    product_callback_data = query.data
    product_index = int(product_callback_data.split('_')[1])

    selected_product = Product.objects.all().order_by('id')[
        product_index - 1]

    if selected_product:

        invoice_text = f"🧾فاکتور شما: \n\n{selected_product.name}\n\n💰قیمت: {selected_product.price}T\n\n 👤تعداد کاربر : دو کاربر\n\n⏳زمان : ۳۰ روز"

        bot.send_message(user_id, invoice_text, reply_markup=Inline_confirmation_keyboard)
    else:
        bot.send_message(user_id, "Product not found.")


