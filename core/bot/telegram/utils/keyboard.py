from telebot import types
from website.models import Product, MajorProduct, Tutorial


class KeyboardCreator:
    def __init__(self):
        pass

    @staticmethod
    def create_reply_keyboard(buttons):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button_row in buttons:
            keyboard.add(*button_row)
        return keyboard

    @staticmethod
    def create_inline_markup(items):
        inline_keyboard_markup = types.InlineKeyboardMarkup()
        for i, item in enumerate(items, start=1):
            inline_button = types.InlineKeyboardButton(
                text=item.name, callback_data=f"p_{i}"
            )
            inline_keyboard_markup.add(inline_button)
        return inline_keyboard_markup

    @staticmethod
    def create_major_inline_markup(items):
        inline_major_keyboard_markup = types.InlineKeyboardMarkup()
        for i, item in enumerate(items, start=1):
            inline_button = types.InlineKeyboardButton(
                text=item.name, callback_data=f"m_{i}"
            )
            inline_major_keyboard_markup.add(inline_button)
        return inline_major_keyboard_markup

    @staticmethod
    def create_inline_markup_tutorial(items):
        inline_keyboard_markup = types.InlineKeyboardMarkup()
        for i, item in enumerate(items, start=1):
            inline_button = types.InlineKeyboardButton(
                text=item.name, callback_data=f"{item.name}", url=item.telegram_id
            )
            inline_keyboard_markup.add(inline_button)
        return inline_keyboard_markup

    @staticmethod
    def create_inline_join_button():
        inline_keyboard_markup = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton("عضو شدم", callback_data="joined")
        inline_keyboard_markup.add(join_button)
        return inline_keyboard_markup


class Keyboards:
    def __init__(self):
        pass

    main_buttons = [
        [types.KeyboardButton("⭐️ خرید سرویس")],
        [
            types.KeyboardButton("👤 اشتراک‌های من"),
            types.KeyboardButton("🧪دریافت سرور تست"),
        ],
        [types.KeyboardButton("💡 راهنما‌ی سرویس"), types.KeyboardButton("💬 پشتیبانی")],
        [types.KeyboardButton("🛍 خرید عمده️"), types.KeyboardButton("👨‍👩‍👧‍👧 معرفی به دوستان")],
    ]
    main_keyboard = KeyboardCreator.create_reply_keyboard(main_buttons)

    products = Product.objects.all()
    product_inline_markup = KeyboardCreator.create_inline_markup(products)

    tutorials = Tutorial.objects.all()
    tutorial_inline_markup = KeyboardCreator.create_inline_markup_tutorial(tutorials)

    major_products = MajorProduct.objects.all()
    major_product_inline_markup = KeyboardCreator.create_major_inline_markup(
        major_products
    )

    confirm_button = types.InlineKeyboardButton(text="تایید", callback_data="confirm")
    DC_button = types.InlineKeyboardButton(text="کد تخفیف دارم", callback_data="discount")
    inline_confirmation_keyboard = types.InlineKeyboardMarkup().add(confirm_button, DC_button)

    card = types.InlineKeyboardButton(text="شماره کارت", callback_data="card")
    trx = types.InlineKeyboardButton(text="ارز دیجیتال ترون", callback_data="trx")
    inline_payment_keyboard = types.InlineKeyboardMarkup().add(card, trx)

    cancel = types.InlineKeyboardButton(text="حذف اشتراک", callback_data="delete")
    inline_delete_subscription = types.InlineKeyboardMarkup().add(cancel)

    inline_keyboard_approve = types.InlineKeyboardMarkup()
    inline_keyboard_approve.row(
        types.InlineKeyboardButton("تایید ✅", callback_data="confirm"),
        types.InlineKeyboardButton("انصراف ❌", callback_data="cancel"),
    )
    join_button_inline = KeyboardCreator.create_inline_join_button()
