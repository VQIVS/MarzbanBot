from telebot import TeleBot
from django.core.files.base import ContentFile
from website.models import (
    Configuration,
    Message,
    ChannelAdmin,
    Product,
    PaymentMethod,
    TelegramChannel,
    Payment,
)
from bot.models import BotUser, Order, Subscription
import os
import django
from bot.keyboard import (
    keyboard,
    inline_keyboard_markup,
    inline_tutorial_markup,
    Inline_confirmation_keyboard,
    Inline_payment_keyboard,
    Inline_cancel_keyboard,
)
from django.db import IntegrityError
from datetime import datetime, timedelta, timezone
from .functions import (
    create_user,
    get_access_token,
    generate_custom_id,
    get_user,
    delete_user,
)

# Get configuration from the db
conf = Configuration.objects.first()
token = conf.token
message_bot = Message.objects.first()
bot = TeleBot(conf.token)
panel = conf.panel_url

# get the access token
access_token = get_access_token(conf.panel_username, conf.panel_password, panel)

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
    bot.send_message(
        user_id, "💬 برای دریافت پشتیبانی به اکانت زیر پیام دهید.\n\n" + support_admin
    )


# Handler for the 'خرید سرویس⭐️' message
@bot.message_handler(func=lambda message: message.text == "خرید سرویس⭐️")
def handler(message):
    user_id = message.from_user.id
    bot.send_message(
        user_id,
        "🤝 لطفاً اشتراک مد نظر خود را انتخاب کنید.",
        reply_markup=inline_keyboard_markup,
    )


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
        invoice_text = f"📄 **فاکتور شما**:\n\n📦 محصول: {selected_product.name}\n\n💵 قیمت: {selected_product.price} تومان\n\n👥 تعداد کاربر: دو کاربر\n\n⏳ زمان: ۳۰ روز"
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
    bot.send_message(
        user_id,
        "💳 لطفاً روش پرداخت خود را انتخاب کنید.",
        reply_markup=Inline_payment_keyboard,
    )


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
            text = f"🏷️ مبلغ: {price} تومان\n\n💳 شماره کارت: {payment_method.card_number}\n\n👤 نام صاحب کارت: {payment_method.holders_name}\n\n📩 پس از پرداخت، رسید خود را داخل بات ارسال کنید و منتظر تایید پرداخت بمانید."

            bot.send_message(user_id, text)
        else:
            bot.send_message(user_id, "No product found for the last order.")
    else:
        bot.send_message(user_id, "No previous order found.")


@bot.callback_query_handler(func=lambda query: query.data == "trx")
def handler(query):
    user_id = query.message.chat.id
    bot.send_message(user_id, "غیرفعال")


@bot.message_handler(content_types=["photo"])
def confirmation(message):
    user_id = message.from_user.id
    last_order = Order.objects.filter(user__user_id=user_id).last()
    product = last_order.product

    # Save the photo
    save_directory = "bot/payment_photos"
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = bot.get_file(file_id)
    file_extension = os.path.splitext(file_info.file_path)[-1]
    unique_filename = f"photo_{file_id}{file_extension}"
    local_photo_path = os.path.join(save_directory, unique_filename)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(local_photo_path, "wb") as new_file:
        new_file.write(downloaded_file)

    # Create Payment object
    payment = Payment.objects.create(
        amount=last_order.product.price,
        timestamp=datetime.now(),
    )

    # Save the photo in the Payment object
    with open(local_photo_path, "rb") as photo_file:
        payment.photo.save(unique_filename, ContentFile(photo_file.read()), save=True)

    # Reply to user
    text = "📥 رسید شما دریافت شد.\n\n⏳ منتظر بمانید تا پرداخت شما تایید شود. با تشکر از صبوری شما! 😊"
    bot.reply_to(message, text)

    # Send photo to the channel
    channel = TelegramChannel.objects.first()
    with open(local_photo_path, "rb") as photo_to_send:
        bot.send_photo(
            channel.address,
            photo_to_send,
            caption=f"User {user_id} Payment Confirmation price: {product.price} TOMANS",
        )


def extract_user_id_from_caption(caption):
    try:
        parts = caption.split()
        if len(parts) < 2:
            raise ValueError("Caption does not contain user ID")

        user_id = int(parts[1])
        return user_id
    except (IndexError, ValueError) as e:
        print(f"Error extracting user ID: {e}")
        return None


@bot.channel_post_handler(content_types=["text"])
def handle_channel_post(message):
    if "confirm" in message.text.lower() and message.reply_to_message:
        user_id = extract_user_id_from_caption(message.reply_to_message.caption)
        last_order = Order.objects.filter(user__user_id=user_id).last()

        if last_order:
            product = last_order.product
            data_limit = product.data_limit
            expiry_utc_time = datetime.now(timezone.utc) + timedelta(
                days=product.expire
            )
            sub_user = generate_custom_id(32)

            user = create_user(
                sub_user, data_limit, expiry_utc_time.timestamp(), access_token, panel
            )

            if user:
                subscription_url = user.get("subscription_url", "")

                if subscription_url:
                    formatted_message = (
                        "🔐 جزئیات اشتراک 🔐\n\n"
                        "👤 نام کاربری: {}\n\n"
                        "⏰ تاریخ انقضا: {}\n\n"
                        "💾 محدودیت داده: {} گیگابایت\n\n"
                        "🔗 لینک اشتراک:\n {}\n\n"
                        "توجه: اشتراک شما فعال شد. جزئیات را در زیر مشاهده کنید.\n"
                    ).format(
                        user["username"],
                        expiry_utc_time.strftime("%Y-%m-%d %H:%M:%S"),
                        data_limit,
                        subscription_url,
                    )

                    bot.send_message(user_id, formatted_message)

                    # Save subscription details to database
                    bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
                    subscription = Subscription.objects.create(
                        user_id=bot_user, sub_user=sub_user
                    )
                    last_order.status = "Completed"
                    last_order.save()
                else:
                    print("No subscription URL available")
            else:
                print("No subscription data available")
                print(access_token)
        else:
            print("No order found for the user")


@bot.message_handler(func=lambda message: message.text == "اشتراک های من👤")
def handler(message):
    user_id = message.chat.id
    bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
    sub_users = Subscription.objects.filter(user_id=bot_user).values_list(
        "sub_user", flat=True
    )
    for sub_user in sub_users:
        user = get_user(
            sub_user, access_token, panel
        )  # Assuming get_user is defined elsewhere
        if user:
            username = user.get("username")
            expire_timestamp = int(user.get("expire"))  # Convert to int
            expire_date = datetime.fromtimestamp(expire_timestamp)
            days_to_expire = (expire_date - datetime.now()).days
            data_limit = user.get("data_limit") / 1024**3
            status = user.get("status")
            used_traffic = user.get("used_traffic") / 1024**3
            subscription_url = user.get("subscription_url")
            formatted_message = (
                "👤 شناسه اشتراک: {}\n\n"
                "⏰ تاریخ انقضا: {} ({} روز دیگر)\n\n"
                "💾 محدودیت داده: {}\n\n"
                "📊 وضعیت: {}\n\n"
                "🚦 ترافیک استفاده شده: {}\n\n"
                "🔗 لینک اشتراک:\n [{}]({})\n\n"
            ).format(
                username,
                expire_date,
                days_to_expire,
                data_limit,
                status,
                used_traffic,
                subscription_url,
            )

            # Check expiration
            if expire_date <= datetime.now() or data_limit - used_traffic <= 0:
                text = "🚫پایان زمان یا حجم اشتراک🚫\n\n" f" شناسه اشتراک: {username}"
                bot.send_message(user_id, text, reply_markup=Inline_cancel_keyboard)
                Subscription.objects.filter(sub_user=sub_user).update(status=True)
                bot.send_message(
                    user_id, "⚠️لطفا اشتراک خود را حذف و دوباره اقدام به خرید بفرمایید⚠️"
                )
            else:
                # Send the formatted message as a Telegram message
                bot.send_message(user_id, formatted_message)
        else:
            print("no subscription data available")


@bot.callback_query_handler(func=lambda query: query.data == "cancel")
def cancel(query):
    user_id = query.message.chat.id
    bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
    subscription_instance = Subscription.objects.filter(
        user_id=bot_user, status=True
    ).first()
    if subscription_instance:
        # Delete the instance
        subscription_instance.delete()

        # Delete the subscription on the server side
        delete_user(subscription_instance.sub_user, access_token, panel)
        bot.send_message(user_id, "🚫اشتراک حذف شد🚫")
    else:
        bot.send_message(user_id, "هیچ اشتراک فعالی یافت نشد.")
