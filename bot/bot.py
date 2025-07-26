import telebot
from config import Config
from bot.handlers import message_handler, admin_handlers

class ScheduleBot:
    def __init__(self):
        self.bot = telebot.TeleBot(Config.BOT_TOKEN)
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(func=lambda msg: True)
        def handle_all_messages(message):
            message_handler.handle_message(self.bot, message)
        
        admin_handlers.setup_admin_handlers(self.bot)

    def run(self):
        print("Бот запущен...")
        self.bot.infinity_polling()