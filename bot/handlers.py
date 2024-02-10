from telebot import TeleBot
from website.models import Configuration, Message, ChannelAdmin, Product, PaymentMethod
from bot.models import BotUser, Order
import os
import django
from bot.keyboard import (
    keyboard,
    inline_keyboard_markup,
    inline_tutorial_markup,
    Inline_confirmation_keyboard,
    Inline_payment_keyboard,
)
from django.db import IntegrityError

# Get configuration from the database
configuration = Configuration.objects.first()
message_bot = Message.objects.first()
token = configuration.token

# Initialize TeleBot with the retrieved token
bot = TeleBot(token)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


# Handler for the '/start' command
@bot.message_handler(["start"])
def start(message):
    user_id = message.from_user.id

    # Try to create a new BotUser instance
    try:
        bot_user = BotUser(user_id=user_id)
        bot_user.save()
    except IntegrityError:
        # If BotUser already exists, pass silently
        pass

    text = message_bot.text
    bot.send_message(user_id, text, reply_markup=keyboard)


# Handler for the 'آموزش ها💡' message
@bot.message_handler(func=lambda message: message.text == "آموزش ها💡")
def handler(message):
    user_id = message.from_user.id
    bot.send_message(
        user_id,
        "لطفا سیستم عامل خود را انتخاب کنید",
        reply_markup=inline_tutorial_markup,
    )


# Handler for the 'پشتیبانی💬' message
@bot.message_handler(func=lambda message: message.text == "پشتیبانی💬")
def handler(message):
    user_id = message.from_user.id
    support_admin = ChannelAdmin.objects.values("telegram_id").first()["telegram_id"]
    bot.send_message(user_id, support_admin)


# Handler for the 'خرید سرویس⭐️' message
@bot.message_handler(func=lambda message: message.text == "خرید سرویس⭐️")
def handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "message", reply_markup=inline_keyboard_markup)


# Handler for creating an invoice when a product is selected
@bot.callback_query_handler(func=lambda query: query.data.startswith("p_"))
def create_invoice(query):
    user_id = query.message.chat.id
    product_callback_data = query.data
    product_index = int(product_callback_data.split("_")[1])

    # Get the BotUser object corresponding to the user_id
    bot_user = BotUser.objects.get(user_id=user_id)

    # Get the selected product
    selected_product = Product.objects.all().order_by("id")[product_index - 1]

    if selected_product:
        invoice_text = f"🧾فاکتور شما: \n\n{selected_product.name}\n\n💰قیمت: {selected_product.price}T\n\n 👤تعداد کاربر : دو کاربر\n\n⏳زمان : ۳۰ روز"
        bot.send_message(
            user_id, invoice_text, reply_markup=Inline_confirmation_keyboard
        )
    else:
        bot.send_message(user_id, "Product not found.")

    # Create an Order object
    order = Order(user=bot_user, product=selected_product, quantity=1, status="pending")
    order.save()


# Handler for confirming the purchase
@bot.callback_query_handler(func=lambda query: query.data == "confirm")
def handle_confirmation(query):
    user_id = query.message.chat.id
    bot.send_message(user_id, "choose", reply_markup=Inline_payment_keyboard)


# Handler for processing payment with a card
@bot.callback_query_handler(func=lambda query: query.data == "card")
def handler(query):
    user_id = query.message.chat.id

    # Retrieve the last order for the user
    last_order = Order.objects.filter(user__user_id=user_id).last()

    if last_order:
        product = last_order.product
        if product:
            price = product.price
            payment_method = (
                PaymentMethod.objects.first()
            )  # Assuming there is only one payment method
            text = f"💳 پرداخت با استفاده از شماره کارت : {price} {payment_method.card_number}"
            bot.send_message(user_id, text)
        else:
            bot.send_message(user_id, "No product found for the last order.")
    else:
        bot.send_message(user_id, "No previous order found.")
