import pandas as pd
from datetime import datetime
from bot.services import auth, schedule
from bot.utils import (
    log_action,
    with_schedule,
    send_formatted_message,
    send_error_message
)

@log_action("User shifts viewed")
@with_schedule
def show_user_shifts(bot, df, chat_id):
    user_name = auth.get_user_name(chat_id)
    shifts = schedule.get_user_shifts(df, user_name)
    
    if shifts.empty:
        return send_formatted_message(bot, chat_id, "🎉 У вас нет запланированных смен!", [])

    lines = []
    for _, row in shifts.iterrows():
        date_str = row["Дата"].strftime("%d.%m")
        weekday_ru = schedule.WEEKDAYS.get(row["Дата"].strftime("%A"), "")
        
        if pd.notna(row.get("Основа")) and row["Основа"] == user_name:
            lines.append(f"│ <b>👨‍💻 Основная</b>:     {date_str} ({weekday_ru})")
        if pd.notna(row.get("Администрирование")) and row["Администрирование"] == user_name:
            lines.append(f"│ <b>💻 Админ</b>:        {date_str} ({weekday_ru})")
        if pd.notna(row.get("Ночь")) and row["Ночь"] == user_name:
            lines.append(f"│ <b>🌙 Ночь</b>:         {date_str} ({weekday_ru})")
    
    send_formatted_message(bot, chat_id, "📅 Ваши ближайшие смены:", lines)

@log_action("Next shift requested")
@with_schedule
def show_next_shift(bot, df, chat_id):
    user_name = auth.get_user_name(chat_id)
    shifts = schedule.get_user_shifts(df, user_name)
    
    if shifts.empty:
        return send_formatted_message(bot, chat_id, "🎉 У вас нет запланированных смен!", [])

    next_shift = shifts.iloc[0]
    date_str = next_shift["Дата"].strftime("%d.%m")
    weekday_ru = schedule.WEEKDAYS.get(next_shift["Дата"].strftime("%A"), "?")

    lines = []
    # Проверка смен пользователя
    shift_checks = [
        ('Основа', '👨‍💻 Основная'),
        ('Ночь', '🌙 Ночь'),
        ('Администрирование', '💻 Администрирование'),
        ('Руководитель', '👑 Руководитель'),
        ('Резерв', '🔄 Резерв'),
        ('Отпуск', '🏖 Отпуск')
    ]
    
    for col, emoji in shift_checks:
        if pd.notna(next_shift.get(col)) and next_shift[col] == user_name:
            lines.append(f"│ {emoji}: {user_name}")

    if lines:
        lines.append("├─────────────────────────────")

    # Дополнительная информация о смене
    additional_checks = [
        ('Администрирование', '💻 Админ'),
        ('Руководитель', '👑 Руководитель'),
        ('Резерв', '🔄 Резерв'),
        ('Отпуск', '🏖 Отпуск')
    ]
    
    for col, emoji in additional_checks:
        if pd.notna(next_shift.get(col)) and next_shift[col] != user_name:
            lines.append(f"│ {emoji}: {next_shift[col]}")

    send_formatted_message(
        bot,
        chat_id,
        f"⬇️ Ваша следующая смена:",
        [f"│ 📅 {date_str} ({weekday_ru})"] + lines
    )

@log_action("Statistics requested")
@with_schedule
def show_statistics(bot, df, chat_id):
    user_name = auth.get_user_name(chat_id)
    past_shifts = df[df["Дата"] < datetime.now().date()]

    stats = {
        "Основная": {"hours": 0, "count": 0},
        "Ночь": {"hours": 0, "count": 0},
        "Администрирование": {"hours": 0, "count": 0},
        "Резерв": {"hours": 0, "count": 0},
    }

    for _, row in past_shifts.iterrows():
        if pd.notna(row.get("Основа")) and row["Основа"] == user_name:
            stats["Основная"]["hours"] += 12
            stats["Основная"]["count"] += 1
        if pd.notna(row.get("Ночь")) and row["Ночь"] == user_name:
            stats["Ночь"]["hours"] += 12
            stats["Ночь"]["count"] += 1
        if pd.notna(row.get("Администрирование")) and row["Администрирование"] == user_name:
            stats["Администрирование"]["hours"] += 9
            stats["Администрирование"]["count"] += 1
        if pd.notna(row.get("Резерв")) and row["Резерв"] == user_name:
            stats["Резерв"]["hours"] += 9
            stats["Резерв"]["count"] += 1

    total_hours = sum(v["hours"] for v in stats.values())

    if total_hours == 0:
        return send_formatted_message(bot, chat_id, "📭 У вас нет данных по отработанным сменам", [])

    lines = [
        f"│ <b>🕒 Всего часов</b>:     <b>{total_hours}</b>",
        "├─────────────────────────────",
        f"│ <b>🔹 Основные смены</b>:  {stats['Основная']['hours']} ч ({stats['Основная']['count']} смен)",
        f"│ <b>🌙 Ночные смены</b>:    {stats['Ночь']['hours']} ч ({stats['Ночь']['count']} смен)",
        f"│ <b>🖥 Администрирование</b>: {stats['Администрирование']['hours']} ч ({stats['Администрирование']['count']} смен)",
        f"│ <b>🔄 Резерв</b>:          {stats['Резерв']['hours']} ч ({stats['Резерв']['count']} смен)"
    ]

    send_formatted_message(bot, chat_id, f"📊 Статистика {user_name}", lines)