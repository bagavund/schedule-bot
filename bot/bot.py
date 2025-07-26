import telebot
from config import Config
from bot.handlers.message_handler import handle_message

class ScheduleBot:
    def __init__(self):
        self.bot = telebot.TeleBot(Config.BOT_TOKEN)
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(func=lambda msg: True)
        def handle_all_messages(message):
            handle_message(self.bot, message)

    def run(self):
        print("Бот запущен...")
        self.bot.infinity_polling()