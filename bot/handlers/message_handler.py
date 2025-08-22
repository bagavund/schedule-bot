from bot.services import auth
from bot.services.user_logging import user_activity_logger
from bot.keyboards import create_main_menu
from bot.utils.menu_utils import handle_menu_action
from bot.utils import (
    log_action,
    send_formatted_message,
    send_error_message
)
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
    
    # ГСМАиЦП команды
    if text_lower == "сегодня":
        from .schedule_handlers import handle_gsma_today
        handle_gsma_today(bot, message)
    elif text_lower == "завтра":
        from .schedule_handlers import handle_gsma_tomorrow
        handle_gsma_tomorrow(bot, message)
    elif text_lower == "выбрать дату":
        from .schedule_handlers import request_gsma_date
        request_gsma_date(bot, chat_id)
    
    # 1 линия команды
    elif text_lower == "сегодня 1л":
        from .first_line_handlers import handle_first_line_today
        handle_first_line_today(bot, message)
    elif text_lower == "завтра 1л":
        from .first_line_handlers import handle_first_line_tomorrow
        handle_first_line_tomorrow(bot, message)
    elif text_lower == "выбрать дату 1л":
        from .first_line_handlers import request_first_line_date
        request_first_line_date(bot, chat_id)
    
    # 2 линия команды
    elif text_lower == "сегодня 2л":
        from .second_line_handlers import handle_second_line_today
        handle_second_line_today(bot, message)
    elif text_lower == "завтра 2л":
        from .second_line_handlers import handle_second_line_tomorrow
        handle_second_line_tomorrow(bot, message)
    elif text_lower == "выбрать дату 2л":
        from .second_line_handlers import request_second_line_date
        request_second_line_date(bot, chat_id)
    
    # Hybris команды
    elif text_lower == "текущая неделя hybris":
        from .hybris_handlers import show_current_hybris_week
        show_current_hybris_week(bot, chat_id)
    elif text_lower == "📞 контакты hybris":
        from .hybris_handlers import show_hybris_contacts
        show_hybris_contacts(bot, chat_id)

    # Добавляем обработку моих смен
    elif text_lower == "будущие смены":
        from .shift_handlers import show_user_shifts
        show_user_shifts(bot, chat_id)
    
    else:
        logger.warning(f"Unknown command: '{text}'")
        bot.send_message(
            chat_id,
            "Неизвестная команда. Используйте меню для навигации.",
            reply_markup=create_main_menu()
        )