from bot.keyboards import (
    create_schedule_submenu,
    create_my_shifts_submenu,
    create_tools_submenu
)

MENU_ACTIONS = {
    "📅 график смен": {
        "text": "Выберите вариант:",
        "keyboard": create_schedule_submenu
    },
    "👤 мои смены": {
        "text": "Ваши смены:",
        "keyboard": create_my_shifts_submenu
    },
    "🛠 инструменты": {
        "text": "Инструменты:",
        "keyboard": create_tools_submenu
    }
}

def handle_menu_action(bot, chat_id, text):
    # Приводим текст к нижнему регистру для сравнения
    normalized_text = text.lower()
    
    # Ищем совпадение с ключами (без учета регистра)
    for key in MENU_ACTIONS.keys():
        if key.lower() == normalized_text:
            action = MENU_ACTIONS[key]
            bot.send_message(
                chat_id,
                action["text"],
                reply_markup=action["keyboard"]()
            )
            return True
    return False