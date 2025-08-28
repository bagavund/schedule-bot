from bot.services import auth
from bot.services.user_logging import user_activity_logger
from bot.keyboards import create_main_menu, create_tools_submenu
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

    # Обработка смены пользователя
    if text.lower() == "сменить пользователя":
        if auth.is_admin_user(chat_id):
            from .auth_handlers import request_switch_user
            request_switch_user(bot, chat_id)
        else:
            auth.deauthorize_user(chat_id)
            from .auth_handlers import request_auth
            request_auth(bot, chat_id)
        return

    # Проверка авторизации (ОСТАЛОСЬ БЕЗ ИЗМЕНЕНИЙ)
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

    # Мои смены
    elif text_lower == "будущие смены":
        from .shift_handlers import show_user_shifts
        show_user_shifts(bot, chat_id)
    
    # Поддержка проекта
    elif text_lower == "💝 поддержать проект":
        show_support_info(bot, chat_id)
    
    else:
        logger.warning(f"Unknown command: '{text}'")
        bot.send_message(
            chat_id,
            "Неизвестная команда. Используйте меню для навигации.",
            reply_markup=create_main_menu()
        )

def show_support_info(bot, chat_id):
    """Показывает информацию о поддержке проекта"""
    support_text = (
        "💝 <b>Поддержать проект</b>\n\n"
        "Если бот полезен для вас, вы можете поддержать его развитие!\n\n"
        "💰 <b>Через TBank (карты):</b>\n"
        "<a href='https://www.tbank.ru/cf/3GKvqCUDmx8'>https://www.tbank.ru/cf/3GKvqCUDmx8</a>\n\n"
        "💎 <b>TON кошелек:</b>\n"
        "<code>UQDLZF19n_Ba17Ch1BN74iu1hJZqxMr_0vKjVlKW1c0jvkaK</code>\n\n"
        "Спасибо за вашу поддержку! 🙏"
    )
    
    # Создаем inline-кнопки
    from telebot import types
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("💳 Перейти в TBank", url="https://www.tbank.ru/cf/3GKvqCUDmx8"),
        types.InlineKeyboardButton("💎 Скопировать TON", callback_data="copy_ton")
    )
    
    bot.send_message(
        chat_id,
        support_text,
        parse_mode="HTML",
        reply_markup=markup,
        disable_web_page_preview=True
    )