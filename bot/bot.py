from telebot import TeleBot
from config import Config
from bot.handlers import message_handler

class ScheduleBot:
    def __init__(self):
        self.bot = TeleBot(Config.BOT_TOKEN)
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(content_types=['text'])
        def handle_all_messages(message):
            message_handler.handle_message(self.bot, message)

    def run(self):
        try:
            print("Бот успешно запущен...")
            self.bot.infinity_polling()
        except Exception as e:
            print(f"Ошибка при запуске бота: {str(e)}")
            input("Нажмите Enter для выхода...")