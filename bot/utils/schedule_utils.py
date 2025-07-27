from datetime import datetime
from functools import wraps
import logging
from typing import Callable, Any  # Добавлен импорт типов

from bot.services import storage
from bot.utils.core_utils import send_error_message
from bot.keyboards import create_main_menu

logger = logging.getLogger(__name__)

def parse_date(date_str: str) -> datetime.date:
    """Парсит дату из строки в формате ДД.ММ или ДД.ММ.ГГГГ"""
    try:
        if '.' in date_str and len(date_str.split('.')) == 2:
            date_str = f"{date_str}.{datetime.now().year}"
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        return None

def with_schedule(func: Callable) -> Callable:
    """Декоратор для загрузки расписания"""
    @wraps(func)
    def wrapper(bot: Any, *args, **kwargs) -> Any:
        try:
            df = storage.load_schedule()
            if df is None:
                chat_id = args[0].chat.id if hasattr(args[0], 'chat') else kwargs.get('chat_id')
                if chat_id:
                    send_error_message(
                        bot,
                        chat_id,
                        "⚠️ Не удалось загрузить файл расписания",
                        reply_markup=create_main_menu()
                    )
                logger.error("Failed to load schedule")
                return
            return func(bot, df, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in with_schedule: {e}", exc_info=True)
            chat_id = args[0].chat.id if hasattr(args[0], 'chat') else kwargs.get('chat_id')
            if chat_id:
                send_error_message(
                    bot,
                    chat_id,
                    "⚠️ Ошибка обработки запроса",
                    reply_markup=create_main_menu()
                )
    return wrapper