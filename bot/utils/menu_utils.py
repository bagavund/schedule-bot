from bot.keyboards import (
    create_gsma_submenu,
    create_first_line_submenu,
    create_second_line_submenu,
    create_tools_submenu,
    create_hybris_menu
)

MENU_ACTIONS = {
    "📊 график гсмаицп": {
        "text": "График ГСМАиЦП:",
        "keyboard": create_gsma_submenu
    },
    "📈 график 1л": {
        "text": "График 1 линии:",
        "keyboard": create_first_line_submenu
    },
    "📉 график 2л": {
        "text": "График 2 линии:",
        "keyboard": create_second_line_submenu
    },
    "📋 график hybris": {
        "text": "График эскалаций Hybris:",
        "keyboard": create_hybris_menu
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