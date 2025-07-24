from telebot import types

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_schedule = types.KeyboardButton("📅 График смен")
    btn_my_shifts = types.KeyboardButton("👤 Мои смены")
    btn_tools = types.KeyboardButton("🛠 Инструменты")
    markup.add(btn_schedule, btn_my_shifts, btn_tools)
    return markup

def create_schedule_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_today = types.KeyboardButton("Сегодня")
    btn_tomorrow = types.KeyboardButton("Завтра")
    btn_next_shift = types.KeyboardButton("Следующая смена")
    btn_select_date = types.KeyboardButton("Выбрать дату")
    btn_back = types.KeyboardButton("🔙 Назад")
    markup.add(btn_today, btn_tomorrow, btn_next_shift, btn_select_date, btn_back)
    return markup

def create_my_shifts_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_all_shifts = types.KeyboardButton("Все мои смены")
    btn_stats = types.KeyboardButton("Моя статистика")
    btn_back = types.KeyboardButton("🔙 Назад")
    markup.add(btn_all_shifts, btn_stats, btn_back)
    return markup

def create_tools_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_switch_user = types.KeyboardButton("Сменить пользователя")
    btn_admin_tools = types.KeyboardButton("Админ-панель")
    btn_back = types.KeyboardButton("🔙 Назад")
    markup.add(btn_switch_user, btn_admin_tools, btn_back)
    return markup