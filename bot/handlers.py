import pandas as pd
from datetime import datetime, timedelta
from bot.services import auth, schedule, storage
from bot.keyboards import create_main_menu, create_test_menu


def handle_message(bot, message):
    """Обрабатывает входящие сообщения и перенаправляет на соответствующие функции."""
    chat_id = message.chat.id
    text = message.text.lower()

    if text == "сменить пользователя":
        auth.deauthorize_user(chat_id)
        request_auth(bot, chat_id)
        return

    if not auth.is_authorized(chat_id):
        request_auth(bot, chat_id)
        return

    if text == "мои смены":
        show_user_shifts(bot, chat_id)
    elif text == "сегодня":
        show_schedule(bot, chat_id, datetime.now().date())
    elif text == "завтра":
        show_schedule(bot, chat_id, datetime.now().date() + timedelta(days=1))
    elif text == "выбрать дату":
        request_date(bot, chat_id)
    elif text == "тестовые функции":
        bot.send_message(chat_id, "Выберите действие:", reply_markup=create_test_menu())
    elif text == "статистика":
        show_statistics(bot, chat_id)
    elif text == "назад в меню":
        show_main_menu(bot, chat_id)
    else:
        try:
            date_str = f"{text}.{datetime.now().year}"
            date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
            show_schedule(bot, chat_id, date_obj)
        except ValueError:
            show_main_menu(bot, chat_id)


def show_statistics(bot, chat_id):
    """Показывает статистику по отработанным сменам."""
    user_name = auth.get_user_name(chat_id)
    df = storage.load_schedule()

    if df is None:
        bot.send_message(chat_id, "⚠️ Ошибка загрузки расписания")
        return

    past_shifts = df[df["Дата"] < datetime.now().date()]

    stats = {
        "Основная": {"hours": 0, "count": 0},
        "Ночь": {"hours": 0, "count": 0},
        "Администрирование": {"hours": 0, "count": 0},
        "Резерв": {"hours": 0, "count": 0},
    }

    for _, row in past_shifts.iterrows():
        if row["Основа"] == user_name:
            stats["Основная"]["hours"] += 12
            stats["Основная"]["count"] += 1
        if row["Ночь"] == user_name:
            stats["Ночь"]["hours"] += 12
            stats["Ночь"]["count"] += 1
        if pd.notna(row["Администрирование"]) and row["Администрирование"] == user_name:
            stats["Администрирование"]["hours"] += 9
            stats["Администрирование"]["count"] += 1
        if pd.notna(row["Резерв"]) and row["Резерв"] == user_name:
            stats["Резерв"]["hours"] += 9
            stats["Резерв"]["count"] += 1
        if pd.notna(row["Руководитель"]) and row["Руководитель"] == user_name:
            stats["Руководитель"]["hours"] += 9
            stats["Руководитель"]["count"] += 1

    total_hours = sum(v["hours"] for v in stats.values())

    if total_hours == 0:
        bot.send_message(chat_id, "📭 У вас нет данных по отработанным сменам")
        return

    response = (
        f"<b>📊 Статистика {user_name}</b>\n"
        "<pre>┌─────────────────────────────\n"
        f"│ <b>🕒 Всего часов</b>:     <b>{total_hours}</b>\n"
        "├─────────────────────────────\n"
        f"│ <b>🔹 Основные смены</b>:  {stats['Основная']['hours']} ч ({stats['Основная']['count']} смен)\n"
        f"│ <b>🌙 Ночные смены</b>:    {stats['Ночь']['hours']} ч ({stats['Ночь']['count']} смен)\n"
        f"│ <b>🖥 Администрирование</b>: {stats['Администрирование']['hours']} ч ({stats['Администрирование']['count']} смен)\n"
        f"│ <b>🔄 Резерв</b>:          {stats['Резерв']['hours']} ч ({stats['Резерв']['count']} смен)\n"
        "└─────────────────────────────</pre>"
    )

    bot.send_message(chat_id, response, parse_mode="HTML")


def request_auth(bot, chat_id):
    """Запрашивает авторизацию у пользователя."""
    msg = bot.send_message(
        chat_id,
        "🔒 Для доступа к боту требуется авторизация.\n\nВведите фамилию и имя:",
    )
    bot.register_next_step_handler(msg, lambda m: process_auth_step(bot, m))


def process_auth_step(bot, message):
    """Обрабатывает ввод данных для авторизации."""
    chat_id = message.chat.id
    user_input = message.text.strip()

    success, response = auth.authorize_user(chat_id, user_input)
    bot.send_message(
        chat_id, response, reply_markup=create_main_menu() if success else None
    )

    if not success:
        request_auth(bot, chat_id)


def show_user_shifts(bot, chat_id):
    """Показывает смены пользователя в фирменном стиле"""
    user_name = auth.get_user_name(chat_id)
    df = storage.load_schedule()
    
    if df is None:
        return bot.send_message(chat_id, "⚠️ Ошибка загрузки расписания", parse_mode="HTML")

    shifts = schedule.get_user_shifts(df, user_name)
    
    if shifts.empty:
        return bot.send_message(chat_id, "🎉 У вас нет запланированных смен!", parse_mode="HTML")

    message = [
        "<b>📅 Ваши ближайшие смены:</b>",
        "<pre>┌─────────────────────────────"
    ]
    
    for _, row in shifts.iterrows():
        date_str = row["Дата"].strftime("%d.%m.%Y")
        weekday_ru = schedule.WEEKDAYS.get(row["Дата"].strftime("%A"), "")
        
        if row["Основа"] == user_name:
            message.append(f"│ <b>👨‍💻 Основная</b>:     {date_str} ({weekday_ru})")
        if pd.notna(row["Администрирование"]) and row["Администрирование"] == user_name:
            message.append(f"│ <b>💻 Админ</b>:        {date_str} ({weekday_ru})")
        if row["Ночь"] == user_name:
            message.append(f"│ <b>🌙 Ночь</b>:         {date_str} ({weekday_ru})")
    
    message.append("└─────────────────────────────</pre>")
    
    bot.send_message(
        chat_id,
        "\n".join(message),
        parse_mode="HTML"
    )


def show_schedule(bot, chat_id, date):
    """Показывает расписание на указанную дату."""
    df = storage.load_schedule()
    if df is None:
        bot.send_message(chat_id, "⚠️ Ошибка загрузки расписания")
        return

    schedule_data = schedule.get_date_schedule(df, date)
    if schedule_data is not None:
        bot.send_message(
            chat_id,
            schedule.format_schedule(schedule_data),
            reply_markup=create_main_menu(),
            parse_mode="HTML",
        )
    else:
        bot.send_message(
            chat_id,
            f"📅 На {date.strftime('%d.%m.%Y')} расписание не найдено.",
            reply_markup=create_main_menu(),
        )


def request_date(bot, chat_id):
    """Запрашивает у пользователя дату для просмотра расписания."""
    msg = bot.send_message(
        chat_id,
        "📅 Введите дату в формате ДД.ММ (например, 25.07):",
        parse_mode="HTML",
    )
    bot.register_next_step_handler(msg, lambda m: process_date_input(bot, m))


def process_date_input(bot, message):
    """Обрабатывает введенную пользователем дату."""
    chat_id = message.chat.id
    try:
        date_str = f"{message.text}.{datetime.now().year}"
        date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
        show_schedule(bot, chat_id, date_obj)
    except ValueError:
        bot.send_message(
            chat_id,
            "❌ Неверный формат даты. Введите дату в формате ДД.ММ "
            "(например, 25.07).\n\nПопробуйте еще раз или вернитесь в меню.",
            reply_markup=create_main_menu(),
            parse_mode="HTML",
        )


def show_main_menu(bot, chat_id):
    """Показывает главное меню бота."""
    bot.send_message(
        chat_id, "Выберите вариант из меню ниже:", reply_markup=create_main_menu()
    )


def change_user(bot, chat_id):
    """Обрабатывает запрос на смену пользователя."""
    auth.deauthorize_user(chat_id)
    bot.send_message(chat_id, "🔒 Введите новые данные для авторизации:")
    request_auth(bot, chat_id)
