import logging
from bot.services import storage
from bot.keyboards import create_main_menu
from bot.utils.response_utils import send_error_message

logger = logging.getLogger(__name__)

def with_schedule(func):
    def wrapper(bot, *args, **kwargs):
        try:
            df = storage.load_schedule()
            if df is None:
                chat_id = args[0].chat.id if hasattr(args[0], 'chat') else kwargs.get('chat_id')
                if chat_id:
                    send_error_message(
                        bot,
                        chat_id,
                        "⚠️ Не удалось загрузить файл расписания. Пожалуйста, сообщите администратору.",
                        reply_markup=create_main_menu()
                    )
                logger.error("Failed to load schedule: file not found or invalid")
                return
            return func(bot, df, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in with_schedule decorator: {e}", exc_info=True)
            chat_id = args[0].chat.id if hasattr(args[0], 'chat') else kwargs.get('chat_id')
            if chat_id:
                send_error_message(
                    bot,
                    chat_id,
                    "⚠️ Произошла системная ошибка при обработке запроса",
                    reply_markup=create_main_menu()
                )
    return wrapper