from django.core.management.base import BaseCommand
from bot.handlers import bot


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        bot.infinity_polling()
