import pandas as pd
from datetime import datetime

WEEKDAYS = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье",
}

SHIFT_DURATIONS = {
    "Основная": 12,
    "Ночь": 12,
    "Администрирование": 9,
    "Резерв": 9,
    "Руководитель": 9,
}

def format_schedule(row):
    """Форматирует информацию о сменах"""
    date_str = row["Дата"].strftime("%d.%m")  # Убрали год
    weekday_en = row["Дата"].strftime("%A")
    weekday_ru = WEEKDAYS.get(weekday_en, weekday_en)
    
    admin = row["Администрирование"] if pd.notna(row["Администрирование"]) else "—"
    reserve = row["Резерв"] if pd.notna(row["Резерв"]) else "—"
    chief = row["Руководитель"] if pd.notna(row["Руководитель"]) else "—"
    vacation = row["Отпуск"] if pd.notna(row["Отпуск"]) else "—"

    return (
        f"<b>📅 {date_str} ({weekday_ru})</b>\n"
        "<pre>┌─────────────────────────────\n"
        f"│ <b>👨‍💻 Основная</b>:     {row['Основа']}\n"
        f"│ <b>💻 Админ</b>:        {admin}\n"
        f"│ <b>🌙 Ночь</b>:         {row['Ночь']}\n"
        f"│ <b>🔄 Резерв</b>:       {reserve}\n"
        "├─────────────────────────────\n"
        f"│ <b>👑 Руководитель</b>: {chief}\n"
        f"│ <b>🏖 Отпуск</b>:       {vacation}\n"
        "└─────────────────────────────</pre>"
    )


def get_user_shifts(df, user_name, only_future=True):
    today = datetime.now().date()

    mask = (
    (df["Основа"] == user_name)
    | (df["Администрирование"] == user_name)
    | (df["Ночь"] == user_name)
    | (df["Руководитель"] == user_name) 
)

    user_shifts = df[mask].copy()

    if only_future:
        user_shifts = user_shifts[user_shifts["Дата"] > today]

    return user_shifts.sort_values("Дата")


def get_date_schedule(df, date):
    schedule = df[df["Дата"] == date]
    return schedule.iloc[0] if not schedule.empty else None
