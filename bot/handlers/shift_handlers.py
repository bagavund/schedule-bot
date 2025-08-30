import pandas as pd
from datetime import datetime
from bot.services import auth
from bot.utils import send_formatted_message, send_error_message
from bot.keyboards import create_main_menu

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
    """Определяет тип смены для пользователя с учетом линий и множественных значений"""
    
    def check_multiple_users(cell_value, user_name):
        """Проверяет, содержится ли пользователь в ячейке с несколькими значениями"""
        if pd.isna(cell_value):
            return False
     
        separators = [',', ';', ' и ', '/', '\\']
        values = str(cell_value)

        for sep in separators:
            if sep in values:
                users = [u.strip() for u in values.split(sep) if u.strip()]
                if user_name in users:
                    return True

        return values.strip() == user_name
    
    if sheet_name == "ГСМАиЦП":
        if check_multiple_users(row.get("Основа"), user_name):
            return "👨‍💻 Основная"
        elif check_multiple_users(row.get("Администрирование"), user_name):
            return "💻 Админ"
        elif check_multiple_users(row.get("Ночь"), user_name):
            return "🌙 Ночь"
        elif check_multiple_users(row.get("Руководитель"), user_name):
            return "👑 Руководитель"
        elif check_multiple_users(row.get("Резерв"), user_name):
            return "🔄 Резерв"
        elif check_multiple_users(row.get("Ведущий специалист"), user_name):
            return "⭐ Ведущий"
    
    elif sheet_name == "1 Линия":
        if check_multiple_users(row.get("Дневное дежурство"), user_name):
            return "🌞 Дневная"
        elif check_multiple_users(row.get("Ночное дежурство"), user_name):
            return "🌙 Ночная"
        elif check_multiple_users(row.get("Резерв"), user_name):
            return "🔄 Резерв"
        elif check_multiple_users(row.get("Старший специалист"), user_name):
            return "👑 Старший"
    
    elif sheet_name == "2 линия":
        if check_multiple_users(row.get("Офис"), user_name):
            return "🏢 Офис"
        elif check_multiple_users(row.get("Аутсорс"), user_name):
            return "🌐 Аутсорс"
        elif check_multiple_users(row.get("Удаленная помощь"), user_name):
            return "💻 Удаленная"
        elif check_multiple_users(row.get("Старший специалист"), user_name):
            return "👨‍💻 Старший"
        elif check_multiple_users(row.get("Руководитель"), user_name):
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

        sheets_to_check = ["1 Линия", "2 линия", "ГСМАиЦП"]
        
        for sheet_name in sheets_to_check:
            try:
                df = pd.read_excel(Config.SCHEDULE_FILE, sheet_name=sheet_name)
                if "Дата" not in df.columns:
                    continue
                    
                df["Дата"] = pd.to_datetime(df["Дата"], dayfirst=True).dt.date
                df = df[df["Дата"] >= today]
                
                for _, row in df.iterrows():
                    shift_type = get_shift_type(row, user_name, sheet_name)
                    if shift_type:
                        weekday = WEEKDAYS.get(row["Дата"].strftime("%A"), "?")
                        all_shifts.append({
                            "date": row["Дата"],
                            "type": shift_type,
                            "line": sheet_name,
                            "display": f"{shift_type} - {row['Дата'].strftime('%d.%m')} ({weekday})"
                        })
                
                if all_shifts:
                    break
                    
            except Exception as e:
                print(f"Ошибка загрузки {sheet_name}: {e}")
                continue

        if not all_shifts:
            send_formatted_message(bot, chat_id, "🎉 У вас нет запланированных смен!", [])
            return
        
        all_shifts.sort(key=lambda x: x["date"])
        
        lines = []
        for shift in all_shifts:
            lines.append(f"│ {shift['display']}")
        
        send_formatted_message(bot, chat_id, f"📅 Будущие смены ({user_name}):", lines)
        
    except Exception as e:
        print(f"Общая ошибка: {e}")
        send_error_message(bot, chat_id, "❌ Ошибка при загрузке смен")
