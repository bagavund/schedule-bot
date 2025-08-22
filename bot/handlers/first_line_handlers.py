import pandas as pd
from datetime import datetime, timedelta  # Добавить timedelta
import logging
from bot.services import storage
from bot.utils import log_action, send_formatted_message, send_error_message
from bot.keyboards import create_main_menu
from bot.utils.schedule_utils import parse_date

logger = logging.getLogger(__name__)

@log_action("First line schedule viewed")
def show_first_line_schedule(bot, chat_id, date):
    """Показывает расписание 1 линии на указанную дату"""
    try:
        df = load_first_line_schedule()
        if df is None or df.empty:
            return send_error_message(
                bot,
                chat_id,
                "Не удалось загрузить график 1 линии",
                reply_markup=create_main_menu()
            )
        
        schedule_data = get_date_first_line_schedule(df, date)
        if schedule_data is not None:
            send_formatted_message(
                bot,
                chat_id,
                f"📈 1 линия на {date.strftime('%d.%m.%Y')}",
                format_first_line_schedule(schedule_data),
                reply_markup=create_main_menu()
            )
        else:
            send_error_message(
                bot,
                chat_id,
                f"На {date.strftime('%d.%m.%Y')} расписание 1 линии не найдено",
                reply_markup=create_main_menu()
            )
        
    except Exception as e:
        logger.error(f"Error showing first line schedule: {e}")
        send_error_message(
            bot,
            chat_id,
            "Ошибка при загрузке графика 1 линии",
            reply_markup=create_main_menu()
        )

def handle_first_line_today(bot, message):
    """Обработчик для кнопки 'Сегодня 1Л'"""
    show_first_line_schedule(bot, message.chat.id, datetime.now().date())

def handle_first_line_tomorrow(bot, message):
    """Обработчик для кнопки 'Завтра 1Л'"""
    show_first_line_schedule(bot, message.chat.id, datetime.now().date() + timedelta(days=1))

def request_first_line_date(bot, chat_id):
    """Запрос даты для графика 1 линии"""
    msg = bot.send_message(
        chat_id,
        "📅 Введите дату в формате ДД.ММ (например, 25.08):",
        parse_mode="HTML",
    )
    bot.register_next_step_handler(msg, lambda m: process_first_line_date_input(bot, m))

def process_first_line_date_input(bot, message):
    """Обработка введенной даты для графика 1 линии"""
    chat_id = message.chat.id
    date_obj = parse_date(message.text)
    
    if date_obj:
        show_first_line_schedule(bot, chat_id, date_obj)
    else:
        send_error_message(
            bot,
            chat_id,
            "Неверный формат даты. Введите дату в формате ДД.ММ (например, 25.08).",
            reply_markup=create_main_menu()
        )

def load_first_line_schedule():
    """Загружает график 1 линии из Excel"""
    try:
        from config import Config
        df = pd.read_excel(Config.SCHEDULE_FILE, sheet_name="1 Линия")
        df["Дата"] = pd.to_datetime(df["Дата"]).dt.date
        return df
    except Exception as e:
        logger.error(f"Error loading first line schedule: {e}")
        return None

def get_date_first_line_schedule(df, date):
    """Получает расписание 1 линии на указанную дату"""
    schedule = df[df["Дата"] == date]
    return schedule.iloc[0] if not schedule.empty else None

def format_first_line_schedule(row):
    """Форматирует информацию о сменах 1 линии"""
    lines = [
        f"│ <b>🌞 Дневное дежурство</b>: {row['Дневное дежурство'] if pd.notna(row['Дневное дежурство']) else '—'}",
        f"│ <b>🔄 Резерв</b>: {row['Резерв'] if pd.notna(row['Резерв']) else '—'}",
        f"│ <b>🌙 Ночное дежурство</b>: {row['Ночное дежурство'] if pd.notna(row['Ночное дежурство']) else '—'}",
        f"│ <b>👑 Старший специалист</b>: {row['Старший специалист'] if pd.notna(row['Старший специалист']) else '—'}"
    ]
    return lines