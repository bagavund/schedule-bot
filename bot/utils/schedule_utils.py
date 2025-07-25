from bot.services import storage
from bot.utils.response_utils import send_error_message

def with_schedule(func):
    def wrapper(bot, *args, **kwargs):
        df = storage.load_schedule()
        if df is None:
            chat_id = args[0].chat.id if hasattr(args[0], 'chat') else kwargs.get('chat_id')
            return send_error_message(bot, chat_id, "Ошибка загрузки расписания")
        return func(bot, df, *args, **kwargs)
    return wrapper