from datetime import datetime
from functools import wraps
import logging
from typing import Callable, Any
import pandas as pd

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

        try:
            return pd.to_datetime(date_str, dayfirst=True).date()
        except:
            return None

def with_schedule(func: Callable) -> Callable:
    """Декоратор для загрузки расписания"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            df = storage.load_schedule()
            if df is None:
                chat_id = None
                bot = None
                for arg in args:
                    if hasattr(arg, 'send_message'):
                        bot = arg
                    if hasattr(arg, 'chat') and hasattr(arg.chat, 'id'):
                        chat_id = arg.chat.id
                        break
                    if isinstance(arg, int):
                        chat_id = arg    
                if not chat_id:
                    chat_id = kwargs.get('chat_id')
                if not bot:
                    bot = kwargs.get('bot')
                
                if chat_id and bot:
                    send_error_message(
                        bot,
                        chat_id,
                        "⚠️ Не удалось загрузить файл расписания",
                        reply_markup=create_main_menu()
                    )
                logger.error("Failed to load schedule")
                return
            return func(*args, df=df, **kwargs)
            
        except Exception as e:
            logger.error(f"Error in with_schedule: {e}", exc_info=True)
            chat_id = None
            bot = None 
            for arg in args:
                if hasattr(arg, 'send_message'):
                    bot = arg
                if hasattr(arg, 'chat') and hasattr(arg.chat, 'id'):
                    chat_id = arg.chat.id
                    break
                if isinstance(arg, int):
                    chat_id = arg            
            if not chat_id:
                chat_id = kwargs.get('chat_id')
            if not bot:
                bot = kwargs.get('bot')
            
            if chat_id and bot:
                send_error_message(
                    bot,
                    chat_id,
                    "⚠️ Ошибка обработки запроса",
                    reply_markup=create_main_menu()
                )
    return wrapper