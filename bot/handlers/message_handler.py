from bot.services import auth
from bot.services.user_logging import user_activity_logger
from bot.keyboards import create_main_menu, create_admin_keyboard
from bot.utils.menu_utils import handle_menu_action
from bot.utils.decorators import log_action
import logging
from telebot import types

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
    if text == "🔙 Выйти из админки":
        bot.send_message(
            chat_id,
            "Вы вышли из админ-панели",
            reply_markup=create_main_menu()
        )
        return
    elif text == "🔙 Назад":
        bot.send_message(
            chat_id,
            "Главное меню:",
            reply_markup=create_main_menu()
        )
        return

    # Обработка админских команд
    if auth.is_admin(chat_id):
        if text == "📢 Рассылка":
            from .admin_handlers import handle_broadcast_start
            handle_broadcast_start(bot, message)
            return
        elif text == "📊 Статистика":
            bot.send_message(
                chat_id, 
                "Функция статистики в разработке",
                reply_markup=create_admin_keyboard()
            )
            return
        elif text.lower() == "админ-панель":
            from .admin_handlers import handle_admin_panel
            handle_admin_panel(bot, message)
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