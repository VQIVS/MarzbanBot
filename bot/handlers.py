from telebot import TeleBot
import os
from io import BytesIO
from telebot import types
from django.core.files.base import ContentFile
from website.models import (
    Configuration,
    Message,
    ChannelAdmin,
    Product,
    PaymentMethod,
    TelegramChannel,
    Payment,
    MajorProduct,
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
    inline_major_keyboard_markup,
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
        major_product = last_order.major_product
        product = last_order.product
        if product:
            price = product.price
            payment_method = (
                PaymentMethod.objects.first()
            )  # Assuming there is only one payment method
            text = f"🏷️ مبلغ: {price} تومان\n\n💳 شماره کارت: {payment_method.card_number}\n\n👤 نام صاحب کارت: {payment_method.holders_name}\n\n📩 پس از پرداخت، رسید خود را داخل بات ارسال کنید و منتظر تایید پرداخت بمانید."

            bot.send_message(user_id, text)
        elif major_product:
            price = major_product.price * last_order.quantity
            formatted_price = "{:,}".format(price)
            payment_method = (
                PaymentMethod.objects.first()
            )  # Assuming there is only one payment method
            text = f"🏷️ مبلغ: {formatted_price} تومان\n\n💳 شماره کارت: {payment_method.card_number}\n\n👤 نام صاحب کارت: {payment_method.holders_name}\n\n📩 پس از پرداخت، رسید خود را داخل بات ارسال کنید و منتظر تایید پرداخت بمانید."
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
            bot.send_message(
                user_id,
                "There was an error processing your payment confirmation. Please try again later.",
            )
            return

        # Get photo information
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)

        # Download photo
        downloaded_file = bot.download_file(file_info.file_path)

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
        bot.reply_to(message, text)

        # Send photo to the channel
        channel = TelegramChannel.objects.first()
        with BytesIO(downloaded_file) as photo_to_send:
            bot.send_photo(channel.address, photo_to_send, caption=caption)
    else:
        bot.send_message(
            user_id,
            "There was an error processing your payment confirmation. Please try again later.",
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


# @bot.channel_post_handler(content_types=["text"])
# def handler(message):
#     if message.reply_to_message:
#         user_id = major_extract_user_id_from_caption(message.reply_to_message.caption)
#         if "approved" in message.text.lower():
#             last_order = Order.objects.filter(user__user_id=user_id).last()
#             if last_order:
#                 quantity = last_order.quantity
#                 major_product = last_order.major_product
#                 data_limit = major_product.data_limit
#                 expiry_utc_time = datetime.now(timezone.utc) + timedelta(days=major_product.expire)
#                 expire_timestamp = expiry_utc_time.timestamp()
#                 on_hold_expire_duration = int(expire_timestamp - datetime.now().timestamp())
#
#                 # Create a directory to store subscription URLs if it doesn't exist
#                 if not os.path.exists("subscription_urls"):
#                     os.makedirs("subscription_urls")
#
#                 # Generate and store subscription URLs for each user
#                 file_content = ""
#                 for i in range(quantity):
#                     username = generate_custom_id(32)
#                     print(f"Creating user {username}...")
#                     response = create_user(username, data_limit, on_hold_expire_duration, access_token, panel)
#                     if response:
#                         subscription_url = response.get("subscription_url")
#                         if subscription_url:
#                             # Store subscription URL in the content
#                             file_content += f"Username: {username}, Subscription URL: {subscription_url}\n"
#                             print(f"Subscription URL for user {username} created and stored")
#                         else:
#                             print(f"Error creating user {username}: No subscription URL returned")
#                     else:
#                         print(f"Error creating user {username}: No response received from server")
#
#                 # Save subscription URLs to a text file
#                 file_path = f"subscription_urls/{user_id}_subscriptions.txt"
#                 with open(file_path, "w") as file:
#                     file.write(file_content)
#                     print(f"Subscription URLs file created and stored for user {user_id}")
#
#                 # Send the text file to the user who placed the order
#                 with open(file_path, "rb") as file:
#                     bot.send_document(user_id, file)
#                     print(f"Subscription URLs file sent to user {user_id}")
#             else:
#                 print("No order found for the user")
#         else:
#             print("Approval keyword not found in the message")
#     else:
#         print("No reply message found")
#
#
def major_extract_user_id_from_caption(caption):
    try:
        parts = caption.split()
        user_index = parts.index("User")
        user_id = int(parts[user_index + 1])
        return user_id
    except (IndexError, ValueError, AttributeError) as e:
        print(f"Error extracting user ID: {e}")
        return None


@bot.message_handler(func=lambda message: message.text == "اشتراک های من👤")
def handler(message):
    user_id = message.chat.id
    bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
    sub_users = Subscription.objects.filter(user_id=bot_user).values_list(
        "sub_user", flat=True
    )
    if not sub_users:
        bot.send_message(user_id, "⚠️شما اشتراک فعالی ندارید⚠️")

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
                "🔗 لینک اشتراک:\n{}\n\n"
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


@bot.message_handler(func=lambda message: message.text == "خرید عمده🛍️")
def handler(message):
    user_id = message.from_user.id
    bot.send_message(
        user_id,
        "🤝 لطفاً اشتراک مد نظر خود را انتخاب کنید.",
        reply_markup=inline_major_keyboard_markup,
    )


@bot.callback_query_handler(func=lambda query: query.data.startswith("m_"))
def handle_product_selection(query):
    user_id = query.message.chat.id
    product_index = int(query.data.split("_")[1])
    selected_product = MajorProduct.objects.all().order_by("id")[product_index - 1]
    bot_user = BotUser.objects.get(user_id=user_id)

    if selected_product:
        bot.send_message(user_id, "🛒 لطفا تعداد را مشخص کنید.")
        bot_user.state = "quantity_input"
        bot_user.selected_product_id = selected_product.id
        bot_user.save()


@bot.message_handler(
    func=lambda message: BotUser.objects.filter(
        user_id=message.chat.id, state="quantity_input"
    ).exists()
)
def handle_quantity_input(message):
    user_id = message.chat.id
    bot_user = BotUser.objects.get(user_id=user_id, state="quantity_input")
    quantity = message.text

    try:
        quantity = int(quantity)
        if quantity <= 9:
            bot.send_message(
                user_id, "⚠️ تعداد وارد شده باید بیشتر از ۹ باشد. لطفاً دوباره تلاش کنید."
            )
            return

        selected_product_id = bot_user.selected_product_id
        selected_product = MajorProduct.objects.get(id=selected_product_id)

        total_price = selected_product.price * quantity
        total_price_formatted = "{:,}".format(total_price)

        invoice_text = (
            f"📄 **فاکتور شما**:\n\n"
            f"📦 محصول: {selected_product.name}\n\n"
            f"💰 قیمت فی هر اشتراک: {selected_product.price:,} تومان\n\n"
            f"👥 تعداد اشتراک: {quantity} کاربر\n\n"
            f"💵 قیمت کل: {total_price_formatted} تومان\n\n"
            f"⏳ زمان: ۳۰ روز"
        )

        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.row(
            types.InlineKeyboardButton("تایید ✅", callback_data="confirm"),
            types.InlineKeyboardButton("انصراف ❌", callback_data="cancel"),
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

        bot.send_message(user_id, invoice_text, reply_markup=inline_keyboard)

    except ValueError:
        bot.send_message(user_id, "⚠️ لطفاً یک عدد معتبر وارد کنید.")


@bot.channel_post_handler(content_types=["text"])
def handle_channel_post(message):
    if message.reply_to_message:
        if "confirm" in message.text.lower():
            handle_confirm_message(message)
            send_confirmation_feedback(message.chat.id)
        elif "approved" in message.text.lower():
            handle_approved_message(message)
            send_approval_feedback(message.chat.id)
        else:
            print("No action defined for this message")
    else:
        print("No reply message found")


def send_confirmation_feedback(channel_id):
    bot.send_message(channel_id, "Confirmation received and processed.")


def send_approval_feedback(channel_id):
    bot.send_message(channel_id, "Order approved and processed.")


def handle_confirm_message(message):
    user_id = extract_user_id_from_caption(message.reply_to_message.caption)
    last_order = Order.objects.filter(user__user_id=user_id).last()

    if last_order:
        process_confirm_message(last_order, user_id)
    else:
        print("No order found for the user")


def process_confirm_message(last_order, user_id):
    product = last_order.product
    data_limit = product.data_limit
    expiry_utc_time = datetime.now(timezone.utc) + timedelta(days=product.expire)
    sub_user = generate_custom_id(32)

    expire_timestamp = expiry_utc_time.timestamp()
    on_hold_expire_duration = int(expire_timestamp - datetime.now().timestamp())

    user = create_user(
        sub_user, data_limit, on_hold_expire_duration, access_token, panel
    )

    if user:
        handle_subscription_success(
            user, user_id, last_order, sub_user, expiry_utc_time, data_limit
        )
    else:
        print("No subscription data available")


def handle_subscription_success(
    user, user_id, last_order, sub_user, expiry_utc_time, data_limit
):
    subscription_url = user.get("subscription_url", "")

    if subscription_url:
        formatted_message = generate_subscription_message(
            user, expiry_utc_time, data_limit, subscription_url
        )

        bot.send_message(user_id, formatted_message)

        # Save subscription details to database
        save_subscription_details(user_id, sub_user, last_order)
    else:
        print("No subscription URL available")


def generate_subscription_message(user, expiry_utc_time, data_limit, subscription_url):
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
    return formatted_message


def save_subscription_details(user_id, sub_user, last_order):
    bot_user, _ = BotUser.objects.get_or_create(user_id=user_id)
    subscription = Subscription.objects.create(user_id=bot_user, sub_user=sub_user)
    last_order.status = "Completed"
    last_order.save()


def handle_approved_message(message):
    user_id = major_extract_user_id_from_caption(message.reply_to_message.caption)
    last_order = Order.objects.filter(user__user_id=user_id).last()

    if last_order:
        process_approved_message(last_order, user_id)
    else:
        print("No order found for the user")


def process_approved_message(last_order, user_id):
    quantity = last_order.quantity
    major_product = last_order.major_product
    data_limit = major_product.data_limit
    expiry_utc_time = datetime.now(timezone.utc) + timedelta(days=major_product.expire)
    expire_timestamp = expiry_utc_time.timestamp()
    on_hold_expire_duration = int(expire_timestamp - datetime.now().timestamp())

    create_and_send_subscription_urls(
        user_id, quantity, data_limit, on_hold_expire_duration
    )


def create_and_send_subscription_urls(
    user_id, quantity, data_limit, on_hold_expire_duration
):
    # Create a directory to store subscription URLs if it doesn't exist
    if not os.path.exists("subscription_urls"):
        os.makedirs("subscription_urls")

    # Generate and store subscription URLs for each user
    file_content = generate_subscription_urls(
        user_id, quantity, data_limit, on_hold_expire_duration
    )

    # Save subscription URLs to a text file
    file_path = save_subscription_urls(user_id, file_content)

    # Send the text file to the user who placed the order
    send_subscription_file(user_id, file_path)


def generate_subscription_urls(user_id, quantity, data_limit, on_hold_expire_duration):
    file_content = ""
    for i in range(quantity):
        username = generate_custom_id(32)
        print(f"Creating user {username}...")
        response = create_user(
            username, data_limit, on_hold_expire_duration, access_token, panel
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
                print(f"Error creating user {username}: No subscription URL returned")
        else:
            print(f"Error creating user {username}: No response received from server")
    return file_content


def save_subscription_urls(user_id, file_content):
    file_path = f"subscription_urls/{user_id}_subscriptions.txt"
    with open(file_path, "w") as file:
        file.write(file_content)
        print(f"Subscription URLs file created and stored for user {user_id}")
    return file_path


def send_subscription_file(user_id, file_path):
    with open(file_path, "rb") as file:
        bot.send_document(user_id, file)
        print(f"Subscription URLs file sent to user {user_id}")
