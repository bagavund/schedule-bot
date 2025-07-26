from bot.services import auth
from bot.keyboards import create_main_menu
from bot.utils.decorators import log_action
from config import Config

ADMINS = Config.load_admins()

def is_admin(chat_id: int) -> bool:
    user_name = get_user_name(chat_id)
    return user_name in ADMINS

@log_action("Auth requested")
def request_auth(bot, chat_id):
    msg = bot.send_message(
        chat_id,
        "🔒 Для доступа к боту требуется авторизация.\n\nВведите фамилию и имя:"
    )
    bot.register_next_step_handler(msg, lambda m: process_auth_step(bot, m))

@log_action("Auth processed")
def process_auth_step(bot, message):
    chat_id = message.chat.id
    user_input = message.text.strip()

    success, response = auth.authorize_user(chat_id, user_input)
    bot.send_message(
        chat_id,
        response,
        reply_markup=create_main_menu() if success else None
    )

    if not success:
        request_auth(bot, chat_id)