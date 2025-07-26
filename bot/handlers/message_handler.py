from bot.services import auth
from bot.services.user_logging import user_activity_logger
from bot.keyboards import create_main_menu
from bot.utils.menu_utils import handle_menu_action
from bot.utils.decorators import log_action
import logging

logger = logging.getLogger(__name__)

@log_action("Message received")
def handle_message(bot, message):
    chat_id = message.chat.id
    text = message.text.strip()
    user_name = auth.get_user_name(chat_id) or "Unauthorized"
    
    # Логирование
    logger.debug(f"Message from {user_name} (ID: {chat_id}): '{text}'")
    user_activity_logger.log_activity(
        user_id=chat_id,
        username=user_name,
        action="Message received",
        details=f"Text: {text[:100]}"
    )

    # Обработка смены пользователя
    if text.lower() == "сменить пользователя":
        auth.deauthorize_user(chat_id)
        from .auth_handlers import request_auth
        request_auth(bot, chat_id)
        return

    # Проверка авторизации
    if not auth.is_authorized(chat_id):
        from .auth_handlers import request_auth
        request_auth(bot, chat_id)
        return

    # Обработка кнопки "Назад"
    if text == "🔙 Назад":
        bot.send_message(
            chat_id,
            "Главное меню:",
            reply_markup=create_main_menu()
        )
        return

    # Обработка главного меню
    if handle_menu_action(bot, chat_id, text):
        return

    # Обработка основных команд
    text_lower = text.lower()
    if text_lower == "сегодня":
        from .schedule_handlers import handle_today
        handle_today(bot, message)
    elif text_lower == "завтра":
        from .schedule_handlers import handle_tomorrow
        handle_tomorrow(bot, message)
    elif text_lower == "все мои смены":
        from .shift_handlers import show_user_shifts
        show_user_shifts(bot, chat_id)
    elif text_lower == "следующая смена":
        from .shift_handlers import show_next_shift
        show_next_shift(bot, chat_id)
    elif text_lower == "моя статистика":
        from .shift_handlers import show_statistics
        show_statistics(bot, chat_id)
    elif text_lower == "выбрать дату":
        from .schedule_handlers import request_date
        request_date(bot, chat_id)
    else:
        logger.warning(f"Unknown command: '{text}'")
        bot.send_message(
            chat_id,
            "Неизвестная команда. Используйте меню для навигации.",
            reply_markup=create_main_menu()
        )