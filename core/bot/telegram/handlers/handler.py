import os
import django
from telebot import TeleBot
from website.models import Configuration, Message
from ..utils.api_management import APIManager
from .operations import MainHandler, OrderHandler, PurchaseHandler, UserHandler, ConfirmationHandler
from bot.models import BotUser
from ..utils.funcs import rollback

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Initializing settings
conf = Configuration.objects.first()
API_token = conf.token
message_bot = Message.objects.first()
panel = conf.panel_url
bot = TeleBot(API_token)
marzban = APIManager(panel)

# Get the access token from Marzban panel
access_token = marzban.get_token(username=conf.panel_username, password=conf.panel_password)

# Initializing operation handlers
main_handler = MainHandler(API_token, panel, access_token)
order_handler = OrderHandler(API_token, panel, access_token)
purchase_handler = PurchaseHandler(API_token, panel, access_token)
user_handler = UserHandler(API_token, panel, access_token)
confirmation = ConfirmationHandler(API_token, panel, access_token)


@bot.message_handler(["start"])
def start(message):
    main_handler.start(message)


@bot.message_handler(func=lambda message: message.text == "💡 راهنما‌ی سرویس")
def tutorial(message):
    main_handler.tutorial(message)


@bot.message_handler(func=lambda message: message.text == "💬 پشتیبانی")
def support(message):
    main_handler.support(message)


@bot.message_handler(func=lambda message: message.text == "⭐️ خرید سرویس")
def service(message):
    main_handler.buy(message)


@bot.message_handler(func=lambda message: message.text == "🛍 خرید عمده️")
def whole_service(message):
    main_handler.whole_buy(message)


@bot.message_handler(func=lambda message: message.text == "🧪دریافت سرور تست")
def test_subscription(message):
    main_handler.test_subscription(message)


@bot.callback_query_handler(func=lambda query: query.data.startswith("p_"))
def create_invoice(query):
    order_handler.create_service_invoice(query)


@bot.callback_query_handler(func=lambda query: query.data == "confirm")
def confirm_order_invoice(query):
    order_handler.confirm_order(query)


@bot.callback_query_handler(func=lambda query: query.data == "trx")
def trx_purchase(query):
    purchase_handler.trx_purchase(query)


@bot.callback_query_handler(func=lambda query: query.data == "card")
def card_purchase(query):
    purchase_handler.card_purchase(query)


@bot.message_handler(func=lambda message: message.text == "👤 اشتراک‌های من")
def get_subscription_data(message):
    user_handler.get_user_data(message)


@bot.callback_query_handler(func=lambda query: query.data == "delete")
def delete_subscription(query):
    user_handler.delete_subscription(query)


@bot.callback_query_handler(func=lambda query: query.data.startswith("m_"))
def whole_service_selection(query):
    order_handler.whole_service_selection(query)


@bot.message_handler(
    func=lambda message: BotUser.objects.filter(
        user_id=message.chat.id, state="quantity_input"
    ).exists()
)
def create_invoice(message):
    order_handler.create_whole_service_invoice(message)


@bot.callback_query_handler(func=lambda query: query.data == "cancel")
def cancel_process(query):
    rollback(query)


@bot.channel_post_handler(content_types=["text"])
def accept_purchase(message):
    confirmation.accept_purchase(message)


@bot.message_handler(content_types=["photo"])
def send_photo(message):
    purchase_handler.send_order_invoice(message)