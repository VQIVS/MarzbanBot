import logging
import os
import time
from datetime import datetime, timedelta, timezone
from io import BytesIO

from bot.models import BotUser, Order, Subscription
from bot.telegram.utils.keyboard import Keyboards
from django.core.files.base import ContentFile
from django.db import IntegrityError
from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.types import Message as msg
from website.models import (
    ChannelAdmin,
    MajorProduct,
    Message,
    Payment,
    PaymentMethod,
    Product,
    TelegramChannel,
)

from core.core import settings

from ..utils.api_management import APIManager
from ..utils.funcs import (
    bytes_to_gb,
    extract_user_id_from_caption,
    generate_user_id,
    major_extract_user_id_from_caption,
)

# Initializing settings
url: str = settings.PANEL_URL
marzban = APIManager(url)
access_token = marzban.get_token(
    username=settings.PANEL_USER, password=settings.PANEL_PASSWORD
)
logging.basicConfig(level=logging.INFO)


class MainHandler:
    def __init__(self, API_token, panel_url, access_token):
        self.bot = TeleBot(API_token)
        self.panel_url = panel_url
        self.access_token = access_token

    def is_member(self, user_id):
        try:
            member_status = self.bot.get_chat_member(self.channel_id, user_id)
            return member_status.status in ["member", "administrator", "creator"]
        except Exception as e:
            print(f"Error checking membership status: {e}")
            return False

    @staticmethod
    def is_banned(user_id):
        return BotUser.objects.filter(user_id=user_id, is_banned=True).exists()

    def start(self, message: msg):
        user_id = message.from_user.id
        try:
            bot_user = BotUser(user_id=user_id)
            bot_user.save()
        except IntegrityError:
            pass

        msg = Message.objects.first()

        self.bot.send_message(user_id, msg, reply_markup=Keyboards.main_keyboard)

    def handle_join(self, query: CallbackQuery):
        user_id = query.from_user.id
        if self.is_member(user_id):
            self.bot.send_message(
                user_id,
                "با تشکر از پیوستن شما به کانال! اکنون میتوانید از ربات استفاده کنید",
                reply_markup=Keyboards.main_keyboard,
            )
        else:
            self.bot.send_message(
                user_id,
                f"لطفا در کانال عضو شوید: https://t.me/{self.channel_username}",
                reply_markup=Keyboards.join_button_inline,
            )

    def tutorial(self, message):
        user_id = message.from_user.id
        text = ("لطفا سیستم عامل خود را انتخاب کنید",)

        self.bot.send_message(
            user_id, text, reply_markup=Keyboards.tutorial_inline_markup
        )

    def support(self, message):
        user_id = message.from_user.id
        support_admin = ChannelAdmin.objects.values("telegram_id").first()[
            "telegram_id"
        ]
        self.bot.send_message(
            user_id,
            "برای ارتباط با پشتیبانی به اکانت زیر پیام دهید.\n\n" + support_admin,
        )

    def buy(self, message):
        user_id = message.from_user.id
        self.bot.send_message(
            user_id,
            "🤝 لطفاً اشتراک مد نظر خود را انتخاب کنید.",
            reply_markup=Keyboards.product_inline_markup,
        )

    def whole_buy(self, message: msg):
        user_id = message.from_user.id
        self.bot.send_message(
            user_id,
            "🤝 لطفاً اشتراک مد نظر خود را انتخاب کنید.",
            reply_markup=Keyboards.major_product_inline_markup,
        )

    def test_subscription(self, message: msg):
        user_id = message.chat.id
        username = "test" + str(user_id)
        user = BotUser.objects.get(user_id=user_id)
        if user.test_status == "True":
            self.bot.send_message(user_id, "شما یک بار سرور تست دریافت کردید")
        else:
            expiry_utc_time = datetime.now(timezone.utc) + timedelta(days=1)
            expire_timestamp = expiry_utc_time.timestamp()
            on_hold_expire_duration = int(expire_timestamp - datetime.now().timestamp())
            response = marzban.create_user(
                username, 0.2, on_hold_expire_duration, access_token
            )
            if response is not None:
                links = response.get("links")

                subscription_url = response.get("subscription_url")
                first_link = links[0] if len(links) > 0 else "لینک اول موجود نیست"
                second_link = links[1] if len(links) > 1 else "لینک دوم موجود نیست"

                subscription_size = "200MB"
                text = (
                    f"🎉 اشتراک تست شما:\n{subscription_url}\n\n"
                    f"🔋 حجم اشتراک شما: {subscription_size}\n\n"
                    f"1. {first_link}\n\n"
                    f"2. {second_link}"
                )

                user.test_status = "True"
                user.save()
                self.bot.send_message(user_id, text)
            else:
                self.bot.send_message(
                    user_id, "خطایی رخ داده است. لطفا دوباره تلاش کنید"
                )

    def refer(self, message):
        referral_link = f"{settings.BOT_URL}?start=ref_{message.chat.id}"
        text = (
            f"🎉🚀به ازای هر شخص که با [لینک معرفی شما]({referral_link}) به ربات بپیوندد و خریدی "
            f"انجام دهد،"
            f"شما یک اشتراک ۱۰ گیگابایتی رایگان دریافت خواهید کرد! 🎁😊\n\n"
            "پس همین الان زود باش! این پیام را برای دوستانت فوروارد کن و بگو از لینک معرفیت "
            "استفاده کنن. 🚀💬"
        )

        self.bot.send_message(message.chat.id, text=text, parse_mode="Markdown")


class OrderHandler(MainHandler):

    # Main services order operations
    def create_service_invoice(self, query: CallbackQuery):
        msg_id = query.message.message_id
        user_id = query.message.chat.id
        product_callback_data = query.data
        product_index = int(product_callback_data.split("_")[1])
        bot_user = BotUser.objects.get(user_id=user_id)
        selected_product = Product.objects.all().order_by("id")[product_index - 1]
        if selected_product:
            invoice_text = f"📄 پیش فاکتور:\n\n📦 محصول: {selected_product.name}\n\n💵 قیمت: {selected_product.price} تومان\n\n👥 تعداد کاربر: بدون محدودیت\n\n⏳ زمان: {selected_product.expire} روز"
            self.bot.edit_message_text(
                message_id=msg_id,
                chat_id=user_id,
                text=invoice_text,
                reply_markup=Keyboards.inline_confirmation_keyboard,
            )
            order = Order(
                user=bot_user, product=selected_product, quantity=1, status="pending"
            )
            order.save()
        else:
            self.bot.send_message(user_id, "Product not found.")

    def confirm_order(self, query: CallbackQuery):
        msg_id = query.message.message_id
        user_id = query.message.chat.id
        self.bot.edit_message_text(
            message_id=msg_id,
            chat_id=user_id,
            text="💳 لطفاً روش پرداخت خود را انتخاب کنید.",
            reply_markup=Keyboards.inline_payment_keyboard,
        )

    # Whole services order operations
    def whole_service_selection(self, query: CallbackQuery):
        msg_id = query.message.message_id
        user_id = query.message.chat.id
        product_index = int(query.data.split("_")[1])
        selected_product = MajorProduct.objects.all().order_by("id")[product_index - 1]
        bot_user = BotUser.objects.get(user_id=user_id)

        if selected_product:
            self.bot.edit_message_text(
                message_id=msg_id,
                chat_id=user_id,
                text="🛒 لطفا تعداد درخواستی را بفرستید.",
            )
            bot_user.state = "quantity_input"
            bot_user.selected_product_id = selected_product.id
            bot_user.save()

    def create_whole_service_invoice(self, message):
        user_id = message.chat.id
        bot_user = BotUser.objects.get(user_id=user_id, state="quantity_input")
        quantity = message.text

        try:
            quantity = int(quantity)
            if quantity <= 9:
                self.bot.send_message(
                    user_id,
                    "⚠️ تعداد وارد شده باید بیشتر از ۹ باشد. لطفاً دوباره تلاش کنید.",
                )
                return

            selected_product_id = bot_user.selected_product_id
            selected_product = MajorProduct.objects.get(id=selected_product_id)

            total_price = selected_product.price * quantity
            total_price_formatted = f"{total_price:,}"

            invoice_text = (
                f"📄 **فاکتور شما**:\n\n"
                f"📦 محصول: {selected_product.name}\n\n"
                f"💰 قیمت فی هر اشتراک: {selected_product.price:,} تومان\n\n"
                f"👥 تعداد اشتراک: {quantity} کاربر\n\n"
                f"💵 قیمت کل: {total_price_formatted} تومان\n\n"
                f"⏳ زمان: لحظه اتصال کاربر"
            )

            bot_user.state = None
            bot_user.selected_product_id = None
            bot_user.save()

            # Save the order after clearing the session data
            order = Order.objects.create(
                user=bot_user,
                major_product=selected_product,
                quantity=quantity,
                status="Pending",
            )

            self.bot.send_message(
                user_id, invoice_text, reply_markup=Keyboards.inline_keyboard_approve
            )

        except ValueError:
            self.bot.send_message(user_id, "⚠️ لطفاً یک عدد معتبر وارد کنید.")


class PurchaseHandler(MainHandler):
    def card_purchase(self, query: CallbackQuery):
        msg_id = query.message.message_id
        user_id = query.message.chat.id
        last_order = Order.objects.filter(user__user_id=user_id).last()
        if last_order:
            major_product = last_order.major_product
            product = last_order.product
            if product:
                price = product.price
                payment_method = PaymentMethod.objects.first()
                text = (
                    f"🏷️ مبلغ: {price} تومان\n\n💳 شماره کارت: {payment_method.card_number}\n\n👤 نام "
                    f"صاحب کارت: {payment_method.holders_name}\n\n📸 لطفاً پس از پرداخت، عکس رسید خود را داخل بات ارسال "
                    f"کرده و منتظر تایید پرداخت بمانید.\n\n📷 تنها عکس رسید پرداخت مورد قبول است. لطفاً رسید پرداخت را "
                    "مستقیماً به صورت تصویر ارسال کنید."
                )
                text = f"🏷️ مبلغ: {price} تومان\n\n💳 شماره کارت: {payment_method.card_number}\n\n👤 نام صاحب کارت: {payment_method.holders_name}\n\n📩 پس از پرداخت، رسید خود را داخل بات ارسال کنید و منتظر تایید پرداخت بمانید."

                payment_methods = PaymentMethod.objects.all()
                formatted_text = ""
                for payment_method in payment_methods:
                    formatted_text += (
                        f"🏷️ مبلغ: {price} تومان\n\n💳 شماره کارت: {payment_method.card_number}\n\n👤 نام "
                        f"صاحب کارت: {payment_method.holders_name}\n\n📸 لطفاً پس از پرداخت، عکس رسید خود را داخل بات ارسال "
                        f"کرده و منتظر تایید پرداخت بمانید.\n\n📷 تنها عکس رسید پرداخت مورد قبول است. لطفاً رسید پرداخت را "
                        "مستقیماً به صورت تصویر ارسال کنید.\n\n"
                    )
                self.bot.edit_message_text(
                    chat_id=user_id, message_id=msg_id, text=formatted_text
                )
            elif major_product:
                price = major_product.price * last_order.quantity
                formatted_price = f"{price:,}"
                payment_methods = PaymentMethod.objects.all()
                formatted_text = ""
                for payment_method in payment_methods:
                    formatted_text += (
                        f"🏷️ مبلغ: {formatted_price} تومان\n\n💳 شماره کارت: {payment_method.card_number}\n\n👤 نام "
                        f"صاحب کارت: {payment_method.holders_name}\n\n📸 لطفاً پس از پرداخت، عکس رسید خود را داخل بات ارسال "
                        f"کرده و منتظر تایید پرداخت بمانید.\n\n📷 تنها عکس رسید پرداخت مورد قبول است. لطفاً رسید پرداخت را "
                        "مستقیماً به صورت تصویر ارسال کنید.\n\n"
                    )
                self.bot.edit_message_text(
                    chat_id=user_id, message_id=msg_id, text=formatted_text
                )
            else:
                self.bot.send_message(user_id, "No product found for the last order.")
        else:
            self.bot.send_message(user_id, "No previous order found.")

    def trx_purchase(self, query: CallbackQuery):
        user_id = query.message.chat.id
        self.bot.send_message(user_id, "غیرفعال")

    def send_order_invoice(self, message):
        user_id = message.from_user.id
        last_order = Order.objects.filter(user__user_id=user_id).last()

        if last_order:
            if last_order.product:
                product_price = last_order.product.price
                caption = (
                    f"User {user_id} Payment Confirmation price: {product_price} TOMANS"
                )
            elif last_order.major_product:
                product_price = last_order.major_product.price * last_order.quantity
                caption = f"User {user_id} Payment Confirmation price: {product_price} TOMANS (خرید عمده)"
            else:
                self.bot.send_message(
                    user_id,
                    "There was an error processing your payment confirmation. Please try again later.",
                )
                return

            # Get photo information
            photo = message.photo[-1]
            file_id = photo.file_id
            file_info = self.bot.get_file(file_id)

            # Download photo
            downloaded_file = self.bot.download_file(file_info.file_path)

            # Create Payment object
            payment = Payment.objects.create(
                amount=product_price,
                timestamp=datetime.now(),
            )

            # Save photo in Payment object
            with BytesIO(downloaded_file) as photo_file:
                payment.photo.save(
                    f"photo_{file_id}.jpg", ContentFile(photo_file.read()), save=True
                )

            # Reply to user
            text = "📥 رسید شما دریافت شد.\n\n⏳ منتظر بمانید تا پرداخت شما تایید شود. با تشکر از صبوری شما! 😊"
            self.bot.reply_to(message, text)

            # Send photo to the channel
            channel = TelegramChannel.objects.first()
            with BytesIO(downloaded_file) as photo_to_send:
                self.bot.send_photo(channel.address, photo_to_send, caption=caption)
        else:
            self.bot.send_message(
                user_id,
                "There was an error processing your payment confirmation. Please try again later.",
            )


class UserHandler(MainHandler):
    def get_user_data(self, message):
        user_id = message.chat.id
        bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
        sub_users = Subscription.objects.filter(user_id=bot_user).values_list(
            "sub_user", flat=True
        )
        if not sub_users:
            self.bot.send_message(user_id, "⚠️ متاسفانه، شما اشتراک فعالی ندارید!")
            return
        for sub_user in sub_users:
            user = marzban.get_user(
                sub_user, access_token
            )  # Assuming get_user is defined elsewhere
            if user:
                username = user.get("username")
                expire_timestamp = user.get("expire")
                if expire_timestamp is None:
                    expire = "on_hold"
                else:
                    expire_timestamp = int(expire_timestamp)  # Convert to int
                    expire_date = datetime.fromtimestamp(expire_timestamp)
                    days_to_expire = (expire_date - datetime.now()).days
                    expire = (expire_date, days_to_expire)

                data_limit = user.get("data_limit", 0) / 1024**3
                status = user.get("status")
                used_traffic = user.get("used_traffic", 0) / 1024**3
                subscription_url = user.get("subscription_url")
                formatted_message = (
                    "👤 شناسه اشتراک: {}\n\n"
                    "⏰ تاریخ انقضا: {} ({} روز دیگر)\n\n"
                    "💾 محدودیت داده: {}\n\n"
                    "📊 وضعیت: {}\n\n"
                    "🚦 ترافیک استفاده شده: {}\n\n"
                    "🔗 لینک اشتراک:\n{}\n\n"
                ).format(
                    username,
                    expire[0] if isinstance(expire, tuple) else expire,
                    (
                        expire[1] if isinstance(expire, tuple) else ""
                    ),  # Use '' if not tuple
                    data_limit,
                    status,
                    used_traffic,
                    subscription_url,
                )

                # Check expiration
                if isinstance(expire, tuple) and (
                    expire[0] <= datetime.now() or data_limit - used_traffic <= 0
                ):
                    text = (
                        "🚫پایان زمان یا حجم اشتراک🚫\n\n" f" شناسه اشتراک: {username}"
                    )
                    self.bot.send_message(
                        user_id, text, reply_markup=Keyboards.inline_delete_subscription
                    )
                    Subscription.objects.filter(sub_user=sub_user).update(status=True)
                    self.bot.send_message(
                        user_id,
                        "⚠️لطفا اشتراک خود را حذف و دوباره اقدام به خرید بفرمایید⚠️",
                    )
                else:
                    self.bot.send_message(user_id, formatted_message)

    def delete_subscription(self, query: CallbackQuery):
        msg_id = query.message.message_id
        user_id = query.message.chat.id
        bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
        subscription_instance = Subscription.objects.filter(
            user_id=bot_user, status=True
        ).first()
        if subscription_instance:
            subscription_instance.delete()
            text = "🚫اشتراک حذف شد🚫"
            # Delete the subscription on the server side
            marzban.delete_user(subscription_instance.sub_user, access_token)
            self.bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=text)


class ConfirmationHandler(MainHandler):

    def handle_block_message(self, message):
        user_id = extract_user_id_from_caption(message.reply_to_message.caption)
        self.ban_user(user_id)

    def ban_user(self, user_id):
        # Ban the user from the bot
        try:
            self.bot.ban_chat_member(self.channel_id, user_id)
            self.bot.send_message(
                user_id,
                "یوزر شما بلاک شده است.برای دریافت اطلاعات بیشتر به پشتیبانی پیام دهید",
            )
            print(f"User {user_id} has been banned.")
        except Exception as e:
            print(f"Error banning user {user_id}: {e}")

        # Delete the user from the database
        BotUser.objects.filter(user_id=user_id).update(is_banned=True)
        self.bot.send_message(user_id, "You have been banned from using this bot.")
        print(f"User {user_id} has been banned.")

    # Handle  service confirmation
    def service_message(self, channel_id):
        self.bot.send_message(
            channel_id, "Service confirmation received and processed."
        )

    def handle_confirm_message(self, message):
        user_id = extract_user_id_from_caption(message.reply_to_message.caption)
        last_order = Order.objects.filter(user__user_id=user_id).last()
        if last_order:
            self.process_confirm_message(last_order, user_id)
        else:
            print("No order found for the user")

    def process_confirm_message(self, last_order, user_id):

        # check and send the referral prize
        self.award_prize(user_id)
        # ================================================================
        product = last_order.product
        data_limit = product.data_limit
        expiry_utc_time = datetime.now(timezone.utc) + timedelta(days=product.expire)
        sub_user = generate_user_id()

        expire_timestamp = expiry_utc_time.timestamp()
        on_hold_expire_duration = int(expire_timestamp - datetime.now().timestamp())

        user = marzban.create_user(
            sub_user, data_limit, on_hold_expire_duration, access_token
        )

        if user:
            self.subscription_success(
                user, user_id, last_order, sub_user, expiry_utc_time, data_limit
            )
        else:
            print("No subscription data available")

    def subscription_success(
        self, user, user_id, last_order, sub_user, expiry_utc_time, data_limit
    ):
        subscription_url = user.get("subscription_url", "")

        if subscription_url:
            formatted_message = self.generate_subscription_message(
                user, expiry_utc_time, data_limit, subscription_url
            )

            self.bot.send_message(user_id, formatted_message)

            self.save_subscription_details(user_id, sub_user, last_order)
        else:
            print("No subscription URL available")

    @staticmethod
    def generate_subscription_message(
        user, expiry_utc_time, data_limit, subscription_url
    ):
        formatted_message = (
            "🔐 مشخصات اشتراک \n\n"
            "👤 نام کاربری: {}\n\n"
            "⏰ تاریخ انقضا: {}\n\n"
            "💾 محدودیت داده: {} گیگابایت\n\n"
            "🔗 لینک اشتراک:\n {}\n\n"
            "✅ اشتراک شما فعال شد\n"
        ).format(
            user["username"],
            expiry_utc_time.strftime("%Y-%m-%d %H:%M:%S"),
            data_limit,
            subscription_url,
        )
        return formatted_message

    @staticmethod
    def save_subscription_details(user_id, sub_user, last_order):
        bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
        subscription = Subscription.objects.create(user_id=bot_user, sub_user=sub_user)
        last_order.status = "Completed"
        last_order.save()

    # Handle whole service confirmation
    def whole_message(self, channel_id):
        self.bot.send_message(channel_id, "Whole Order approved and processed.")

    @staticmethod
    def generate_subscription_urls(
        user_id, quantity, data_limit, on_hold_expire_duration
    ):
        file_content = ""
        for i in range(quantity):
            username = generate_user_id()
            print(f"Creating user {username}...")

            response = marzban.create_user(
                username, data_limit, on_hold_expire_duration, access_token
            )

            if response:
                subscription_url = response.get("subscription_url")
                if subscription_url:
                    # Store subscription URL in the content
                    file_content += (
                        f"Username: {username}, Subscription URL: {subscription_url}\n"
                    )
                    print(f"Subscription URL for user {username} created and stored")
                else:
                    print(
                        f"Error creating user {username}: No subscription URL returned"
                    )
            else:
                print(
                    f"Error creating user {username}: No response received from server"
                )
        return file_content

    @staticmethod
    def save_subscription_urls(user_id, file_content):
        file_path = f"subscription_urls/{user_id}_subscriptions.txt"
        with open(file_path, "w") as file:
            file.write(file_content)
            print(f"Subscription URLs file created and stored for user {user_id}")
        return file_path

    def send_subscription_file(self, user_id, file_path):
        with open(file_path, "rb") as file:
            self.bot.send_document(user_id, file)
            print(f"Subscription URLs file sent to user {user_id}")
            print(f"Subscription URLs file sent to user {user_id}")

    def create_and_send_subscription_urls(
        self, user_id, quantity, data_limit, on_hold_expire_duration
    ):

        if not os.path.exists("subscription_urls"):
            os.makedirs("subscription_urls")

        file_content = self.generate_subscription_urls(
            user_id, quantity, data_limit, on_hold_expire_duration
        )

        # Save subscription URLs to a text file
        file_path = self.save_subscription_urls(user_id, file_content)

        # Send the text file to the user who placed the order
        self.send_subscription_file(user_id, file_path)

    def process_approved_message(self, last_order, user_id):
        quantity = last_order.quantity
        major_product = last_order.major_product
        data_limit = major_product.data_limit
        expiry_utc_time = datetime.now(timezone.utc) + timedelta(
            days=major_product.expire
        )
        expire_timestamp = expiry_utc_time.timestamp()
        on_hold_expire_duration = int(expire_timestamp - datetime.now().timestamp())

        self.create_and_send_subscription_urls(
            user_id, quantity, data_limit, on_hold_expire_duration
        )

    def handle_approved_message(self, message):
        user_id = major_extract_user_id_from_caption(message.reply_to_message.caption)
        last_order = Order.objects.filter(user__user_id=user_id).last()

        if last_order:
            self.process_approved_message(last_order, user_id)
        else:
            print("No order found for the user")

    def award_prize(self, user_id):
        user = BotUser.objects.filter(user_id=user_id).first()
        if not user.has_received_prize and user.invited_by is not None:
            ref_id = user.invited_by
            username = f"Prize_{ref_id}"
            expiry_utc_time = datetime.now(timezone.utc) + timedelta(days=31)
            expire_timestamp = expiry_utc_time.timestamp()
            on_hold_expire_duration = int(expire_timestamp - datetime.now().timestamp())
            prize = marzban.create_user(
                username, 10, on_hold_expire_duration, access_token
            )
            if prize is not None:
                subscription_url = prize.get("subscription_url")
                subscription_size = "10GB"
                usage_method = "از دکمه راهنمای سرویس استفاده کنید"
                text = (
                    f"تبریک شما برنده جایزه ۱۰ گیگابایتی ما شدید🎉 "
                    f"🎉 اشتراک شما:\n{subscription_url}\n\n"
                    f"🔋 حجم اشتراک شما: {subscription_size}\n\n"
                    f"🔍 نحوه استفاده: {usage_method}"
                )
                self.bot.send_message(ref_id, text)
            user.has_received_prize = True
            user.save()

    def accept_purchase(self, message):
        if message.reply_to_message:
            if "confirm" in message.text.lower():
                self.handle_confirm_message(message)
                self.service_message(message.chat.id)
            elif "approved" in message.text.lower():
                self.handle_approved_message(message)
                self.whole_message(message.chat.id)
            elif "block" in message.text.lower():
                self.handle_block_message(message)
                self.bot.send_message(
                    message.chat.id, "User has been banned and data removed."
                )
            else:
                print("No action defined for this message")
        else:
            print("No reply message found")


class SubscriptionManager:
    def __init__(self, bot):
        self.bot = bot

    def check_subscriptions(self):
        while True:
            # Get all bot users
            bot_users = BotUser.objects.all()

            # Iterate over each bot user
            for bot_user in bot_users:
                # Get subscriptions for the current user
                subscriptions = Subscription.objects.filter(user_id=bot_user)
                if subscriptions:

                    # Iterate over each subscription
                    for subscription in subscriptions:
                        sub_user_id = subscription.sub_user
                        user_data = marzban.get_user(sub_user_id, access_token)
                        if user_data:
                            expire_time = user_data.get("expire")
                            data_limit_bytes = user_data.get("data_limit", 0)
                            data_limit_gb = bytes_to_gb(data_limit_bytes)
                            if user_data.get("status") == "active" and (
                                expire_time is not None
                                and (
                                    data_limit_gb < 1
                                    or datetime.fromtimestamp(expire_time)
                                    <= datetime.now() + timedelta(days=3)
                                )
                            ):
                                user_id = subscription.user_id
                                data_limit = user_data.get("data_limit") / (1024**3)
                                expire_time_formatted = datetime.fromtimestamp(
                                    expire_time
                                ).strftime("%Y-%m-%d %H:%M:%S")
                                notification_message = (
                                    f"🪫اشتراک شما رو به اتمام است\n\n"
                                    f" آیدی اشتراک شما: {sub_user_id}\n\n\n"
                                    f"حجم باقی مانده: 🪫{data_limit}\n"
                                    f"زمان انقضا: {expire_time_formatted}\n"
                                )
                                try:
                                    self.bot.send_message(user_id, notification_message)
                                    logging.info(
                                        f"Notified user {user_id} about subscription status."
                                    )
                                except Exception as e:
                                    logging.error(
                                        f"Failed to send message to user {user_id}: {e}"
                                    )
                        else:
                            logging.error(
                                f"Failed to get user data for subscription: {subscription.id}"
                            )

            time.sleep(60 * 60 * 12)

    def delete_subscriptions(self, bot):

        bot_users = BotUser.objects.all()
        for bot_user in bot_users:
            # Get subscriptions for the current user
            subscriptions = Subscription.objects.filter(user_id=bot_user)
            if subscriptions:
                for subscription in subscriptions:
                    sub_user_id = subscription.sub_user
                    user_data = marzban.get_user(sub_user_id, access_token)
                    self.bot.delete_subscription()
