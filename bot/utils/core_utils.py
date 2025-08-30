from typing import List, Callable, Any 
from telebot import types
from bot.services.auth import get_user_name 

def get_chat_id_from_args(*args, **kwargs) -> int:
    """Извлекает chat_id из аргументов функции"""
    for arg in args:
        if hasattr(arg, 'chat') and hasattr(arg.chat, 'id'):
            return arg.chat.id
    return kwargs.get('chat_id')

def log_action(action_name: str) -> Callable:
    """Декоратор для логирования действий пользователя"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            chat_id = get_chat_id_from_args(*args, **kwargs)
            user_name = get_user_name(chat_id) if chat_id else "Unknown"
            
            details = ""
            for arg in args:
                if hasattr(arg, 'text'):
                    details = f"Text: {arg.text[:100]}"
                    break
            
            from bot.services.user_logging import user_activity_logger
            user_activity_logger.log_activity(
                user_id=chat_id,
                username=user_name,
                action=action_name,
                details=details
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def send_formatted_message(
    bot: Any,
    chat_id: int,
    header: str,
    lines: List[str],
    reply_markup: types.ReplyKeyboardMarkup = None
) -> None:
    """Отправка форматированного сообщения"""
    message = [f"<b>{header}</b>", "<pre>┌─────────────────────────────"]
    message.extend(lines)
    message.append("└─────────────────────────────</pre>")
    bot.send_message(chat_id, "\n".join(message), 
                   parse_mode="HTML", 
                   reply_markup=reply_markup)

def send_error_message(
    bot: Any,
    chat_id: int,
    text: str,
    reply_markup: types.ReplyKeyboardMarkup = None
) -> None:
    """Отправка сообщения об ошибке"""
    bot.send_message(chat_id, f"⚠️ {text}", 
                   parse_mode="HTML",
                   reply_markup=reply_markup)