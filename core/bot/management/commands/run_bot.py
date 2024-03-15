import os
import sys
import time

from django.core.management import BaseCommand
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bot.telegram.handlers.handler import bot


class Watcher(FileSystemEventHandler):
    def __init__(self):
        self.modified = False

    def on_modified(self, event):
        if not self.modified:
            # Check if the modified file is not a JPG or TXT file
            filename, extension = os.path.splitext(event.src_path)
            if extension.lower() not in ['.jpg', '.txt']:
                print("File modified. Reloading bot...")
                self.modified = True
                time.sleep(2)  # Add a small delay to prevent rapid restarts
                os.execv(sys.executable, ["python"] + sys.argv)


def run_bot():
    event_handler = Watcher()
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



