from bot.telegram.handlers.handler import bot
from django.core.management.base import BaseCommand


def run_bot():
    try:
        bot.infinity_polling()
        print("Bot is running")
    except KeyboardInterrupt:
        pass  # Stop the bot gracefully if KeyboardInterrupt is received


class Command(BaseCommand):
    help = "Run the Telegram bot"

    def handle(self, *args, **kwargs):
        run_bot()
