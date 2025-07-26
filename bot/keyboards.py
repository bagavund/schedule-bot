from telebot import types

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("📅 График смен"),
        types.KeyboardButton("👤 Мои смены")
    )
    markup.row(
        types.KeyboardButton("🛠 Инструменты")
    )
    return markup

def create_schedule_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Сегодня"), types.KeyboardButton("Завтра"))
    markup.row(types.KeyboardButton("Выбрать дату"), types.KeyboardButton("🔙 Назад"))
    return markup

def create_my_shifts_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Все мои смены"), types.KeyboardButton("Следующая смена"))
    markup.row(types.KeyboardButton("Моя статистика"), types.KeyboardButton("🔙 Назад"))
    return markup

def create_tools_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Сменить пользователя"))
    markup.row(types.KeyboardButton("🔙 Назад"))
    return markup