from telebot import types


def create_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("Мои смены")
    btn2 = types.KeyboardButton("Сегодня")
    btn3 = types.KeyboardButton("Завтра")
    btn4 = types.KeyboardButton("Выбрать дату")
    btn5 = types.KeyboardButton("Тестовые функции")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def create_test_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Статистика"))
    markup.add(types.KeyboardButton("Сменить пользователя"))
    markup.add(types.KeyboardButton("Назад в меню"))
    return markup
