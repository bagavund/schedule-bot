from bot.services import auth
from bot.keyboards import create_main_menu

from bot.keyboards import (
    create_main_menu,
    create_schedule_submenu,
    create_my_shifts_submenu,
    create_tools_submenu
)
from bot.utils.decorators import log_action

@log_action("Main menu action")
def handle_main_menu(bot, message):
    text = message.text.lower()
    
    if text == "📅 график смен":
        bot.send_message(
            message.chat.id,
            "Выберите вариант:",
            reply_markup=create_schedule_submenu()
        )
    elif text == "👤 мои смены":
        bot.send_message(
            message.chat.id,
            "Ваши смены:",
            reply_markup=create_my_shifts_submenu()
        )
    elif text == "🛠 инструменты":
        bot.send_message(
            message.chat.id,
            "Инструменты:",
            reply_markup=create_tools_submenu()
        )