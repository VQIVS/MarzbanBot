from django.core.management.base import BaseCommand
from bot.telegram.handlers.handler import bot
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.modified = False

    def on_modified(self, event):
        if not self.modified:
            print("File modified. Reloading bot...")
            self.modified = True
            time.sleep(2)  # Add a small delay to prevent rapid restarts
            os.execv(sys.executable, ["python"] + sys.argv)


def run_bot():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    try:
        bot.infinity_polling()
    finally:
        observer.stop()
        observer.join()


class Command(BaseCommand):
    help = "Run the Telegram bot"

    def handle(self, *args, **kwargs):
        run_bot()
