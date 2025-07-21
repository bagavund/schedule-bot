from bot.bot import ScheduleBot

if __name__ == '__main__':
    try:
        bot = ScheduleBot()
        bot.run()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        input("Нажмите Enter для выхода...")