from telebot import types

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("📊 График ГСМАиЦП"),
        types.KeyboardButton("📈 График 1Л")
    )
    markup.row(
        types.KeyboardButton("📋 График Hybris"),
        types.KeyboardButton("🛠 Инструменты")
    )
    return markup

def create_gsma_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Сегодня ГСМА"), types.KeyboardButton("Завтра ГСМА"))
    markup.row(types.KeyboardButton("Выбрать дату ГСМА"), types.KeyboardButton("🔙 Назад"))
    return markup

def create_first_line_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Сегодня 1Л"), types.KeyboardButton("Завтра 1Л"))
    markup.row(types.KeyboardButton("Выбрать дату 1Л"), types.KeyboardButton("🔙 Назад"))
    return markup

def create_tools_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Сменить пользователя"))
    markup.row(types.KeyboardButton("🔙 Назад"))
    return markup

def create_hybris_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Текущая неделя Hybris"))
    markup.row(types.KeyboardButton("🔙 Назад"))
    return markup