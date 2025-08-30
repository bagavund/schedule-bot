import logging
from telebot import types
from bot.services.auth import (
    authorize_user_by_username, 
    authorize_user_legacy, 
    is_admin_user,
    get_user_name,
    deauthorize_user
)
from bot.keyboards import create_main_menu
from bot.utils import log_action, send_error_message

logger = logging.getLogger(__name__)

@log_action("Auth requested")
def request_auth(bot, chat_id):
    """Запрос авторизации с информацией о логине пользователя"""
    try:
        user = bot.get_chat(chat_id)
        username = f"@{user.username}" if user.username else None
        
        if username:
            message_text = (
                f"🔒 Для доступа к боту требуется авторизация.\n\n"
                f"Введите ваши фамилию и имя:"
            )
        else:
            message_text = (
                f"🔒 Для доступа к боту требуется авторизация.\n\n"
                f"⚠️ У вашего аккаунта не установлен username (@логин)\n\n"
                f"Введите ваши фамилию и имя:"
            )
            
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        message_text = "🔒 Для доступа к боту требуется авторизация.\n\nВведите ваши фамилию и имя:"
    
    msg = bot.send_message(chat_id, message_text)
    bot.register_next_step_handler(msg, lambda m: process_auth_step(bot, m))

@log_action("Auth processed")
def process_auth_step(bot, message):
    """Обработка введенных данных авторизации"""
    chat_id = message.chat.id
    user_input = message.text.strip()

    success, response = authorize_user_by_username(message, user_input)
    
    if success:
        bot.send_message(chat_id, response, reply_markup=create_main_menu())
    else:
        if "Неверные данные" in response or "Ожидается:" in response:
            msg = bot.send_message(chat_id, response)
            bot.register_next_step_handler(msg, lambda m: process_auth_step(bot, m))
        else:
            bot.send_message(chat_id, response)
            request_auth(bot, chat_id)

@log_action("User switch requested")
def request_switch_user(bot, chat_id):
    """Запрос на переключение пользователя (только для администратора)"""
    if not is_admin_user(chat_id):
        send_error_message(bot, chat_id, "❌ Эта функция доступна только администратору.")
        return
    
    current_user = get_user_name(chat_id)
    
    msg = bot.send_message(
        chat_id,
        f"🔒 Переключение пользователя\n\n"
        f"Текущий пользователь: {current_user}\n"
        f"Введите фамилию и имя пользователя для переключения:",
        reply_markup=create_main_menu()
    )
    bot.register_next_step_handler(msg, lambda m: process_switch_user(bot, m))

@log_action("User switch processed")
def process_switch_user(bot, message):
    """Обработка переключения пользователя"""
    chat_id = message.chat.id
    user_input = message.text.strip()

    if not is_admin_user(chat_id):
        send_error_message(bot, chat_id, "❌ Эта функция доступна только администратору.")
        return

    if user_input.lower() in ['отмена', 'назад', 'cancel']:
        bot.send_message(
            chat_id,
            "❌ Переключение пользователя отменено.",
            reply_markup=create_main_menu()
        )
        return

    success, response = authorize_user_legacy(chat_id, user_input)
    
    if success:
        bot.send_message(chat_id, response, reply_markup=create_main_menu())
    else:
        msg = bot.send_message(
            chat_id,
            f"{response}\n\nПопробуйте ещё раз или введите 'отмена' для отмены:"
        )
        bot.register_next_step_handler(msg, lambda m: process_switch_user(bot, m))