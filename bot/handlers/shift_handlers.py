import pandas as pd
from datetime import datetime
from bot.services import auth
from bot.utils import send_formatted_message, send_error_message
from bot.keyboards import create_main_menu

# Словарь дней недели
WEEKDAYS = {
    "Monday": "Пн",
    "Tuesday": "Вт",
    "Wednesday": "Ср",
    "Thursday": "Чт",
    "Friday": "Пт",
    "Saturday": "Сб",
    "Sunday": "Вс"
}

def get_shift_type(row, user_name, sheet_name):
    """Определяет тип смены для пользователя с учетом линий"""
    if sheet_name == "ГСМАиЦП":
        if row.get("Основа") == user_name:
            return "👨‍💻 Основная"
        elif row.get("Администрирование") == user_name:
            return "💻 Админ"
        elif row.get("Ночь") == user_name:
            return "🌙 Ночь"
        elif row.get("Руководитель") == user_name:
            return "👑 Руководитель"
        elif row.get("Резерв") == user_name:
            return "🔄 Резерв"
    
    elif sheet_name == "1 Линия":
        if pd.notna(row.get("Дневное дежурство")) and user_name in str(row.get("Дневное дежурство", "")):
            return "🌞 Дневная"
        elif row.get("Ночное дежурство") == user_name:
            return "🌙 Ночная"
        elif row.get("Резерв") == user_name:
            return "🔄 Резерв"
        elif row.get("Старший специалист") == user_name:
            return "👑 Старший"
    
    elif sheet_name == "2 линия":
        if row.get("Офис") == user_name:
            return "🏢 Офис"
        elif row.get("Аутсорс") == user_name:
            return "🌐 Аутсорс"
        elif pd.notna(row.get("Удаленная помощь")) and user_name in str(row.get("Удаленная помощь", "")):
            return "💻 Удаленная"
        elif row.get("Старший специалист") == user_name:
            return "👨‍💻 Старший"
        elif row.get("Руководитель") == user_name:
            return "👑 Руководитель"
    
    return None

def show_user_shifts(bot, chat_id):
    """Показывает будущие смены пользователя из всех линий"""
    try:
        user_name = auth.get_user_name(chat_id)
        if not user_name:
            send_error_message(bot, chat_id, "❌ Вы не авторизованы")
            return
        
        from config import Config
        today = datetime.now().date()
        all_shifts = []

        # Сначала проверяем 1 линию
        try:
            df_first = pd.read_excel(Config.SCHEDULE_FILE, sheet_name="1 Линия")
            df_first["Дата"] = pd.to_datetime(df_first["Дата"]).dt.date
            df_first = df_first[df_first["Дата"] >= today]
            
            for _, row in df_first.iterrows():
                shift_type = get_shift_type(row, user_name, "1 Линия")
                if shift_type:
                    weekday = WEEKDAYS.get(row["Дата"].strftime("%A"), "?")
                    all_shifts.append({
                        "date": row["Дата"],
                        "type": shift_type,
                        "line": "1Л",
                        "display": f"{shift_type} - {row['Дата'].strftime('%d.%m')} ({weekday})"
                    })
        except Exception as e:
            print(f"Ошибка загрузки 1 линии: {e}")

        # Если нашли смены в 1 линии, НЕ проверяем другие линии
        if all_shifts:
            # Сортируем по дате
            all_shifts.sort(key=lambda x: x["date"])
            
            # Формируем сообщение
            lines = []
            for shift in all_shifts:
                lines.append(f"│ {shift['display']}")
            
            send_formatted_message(bot, chat_id, f"📅 Будущие смены ({user_name}):", lines)
            return

        # Если в 1 линии не нашли, проверяем 2 линию
        try:
            df_second = pd.read_excel(Config.SCHEDULE_FILE, sheet_name="2 линия")
            df_second["Дата"] = pd.to_datetime(df_second["Дата"]).dt.date
            df_second = df_second[df_second["Дата"] >= today]
            
            for _, row in df_second.iterrows():
                shift_type = get_shift_type(row, user_name, "2 линия")
                if shift_type:
                    weekday = WEEKDAYS.get(row["Дата"].strftime("%A"), "?")
                    all_shifts.append({
                        "date": row["Дата"],
                        "type": shift_type,
                        "line": "2Л",
                        "display": f"{shift_type} - {row['Дата'].strftime('%d.%m')} ({weekday})"
                    })
        except Exception as e:
            print(f"Ошибка загрузки 2 линии: {e}")

        # Если нашли смены во 2 линии, НЕ проверяем ГСМАиЦП
        if all_shifts:
            # Сортируем по дате
            all_shifts.sort(key=lambda x: x["date"])
            
            # Формируем сообщение
            lines = []
            for shift in all_shifts:
                lines.append(f"│ {shift['display']}")
            
            send_formatted_message(bot, chat_id, f"📅 Будущие смены ({user_name}):", lines)
            return

        # Если не нашли в 1 и 2 линиях, проверяем ГСМАиЦП
        try:
            df_gsma = pd.read_excel(Config.SCHEDULE_FILE, sheet_name="ГСМАиЦП")
            df_gsma["Дата"] = pd.to_datetime(df_gsma["Дата"]).dt.date
            df_gsma = df_gsma[df_gsma["Дата"] >= today]
            
            for _, row in df_gsma.iterrows():
                shift_type = get_shift_type(row, user_name, "ГСМАиЦП")
                if shift_type:
                    weekday = WEEKDAYS.get(row["Дата"].strftime("%A"), "?")
                    all_shifts.append({
                        "date": row["Дата"],
                        "type": shift_type,
                        "line": "ГСМА",
                        "display": f"{shift_type} - {row['Дата'].strftime('%d.%m')} ({weekday})"
                    })
        except Exception as e:
            print(f"Ошибка загрузки ГСМАиЦП: {e}")

        if not all_shifts:
            send_formatted_message(bot, chat_id, "🎉 У вас нет запланированных смен!", [])
            return
        
        # Сортируем по дате
        all_shifts.sort(key=lambda x: x["date"])
        
        # Формируем сообщение
        lines = []
        for shift in all_shifts:
            lines.append(f"│ {shift['display']}")
        
        send_formatted_message(bot, chat_id, f"📅 Будущие смены ({user_name}):", lines)
        
    except Exception as e:
        print(f"Общая ошибка: {e}")
        send_error_message(bot, chat_id, "❌ Ошибка при загрузке смен")