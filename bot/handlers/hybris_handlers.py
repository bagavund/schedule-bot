import pandas as pd
from datetime import datetime
import logging
from bot.services import storage
from bot.utils import log_action, send_formatted_message, send_error_message
from bot.keyboards import create_main_menu

# Добавляем логгер
logger = logging.getLogger(__name__)

@log_action("Hybris schedule viewed")
def show_hybris_schedule(bot, chat_id):
    """Показывает весь график Hybris"""
    try:
        df = load_hybris_schedule()
        if df is None or df.empty:
            return send_error_message(
                bot,
                chat_id,
                "Не удалось загрузить график Hybris",
                reply_markup=create_main_menu()
            )
        
        lines = []
        for _, row in df.iterrows():
            week = row["Неделя"] if pd.notna(row["Неделя"]) else "Не указано"
            first_esc = row["Первая эскалация"] if pd.notna(row["Первая эскалация"]) else "—"
            second_esc = row["Вторая эскалация"] if pd.notna(row["Вторая эскалация"]) else "—"
            
            lines.append(f"│ <b>📅 Неделя</b>: {week}")
            lines.append(f"│ <b>👑 1-я эскалация</b>: {first_esc}")
            lines.append(f"│ <b>🔹 2-я эскалация</b>: {second_esc}")
            lines.append("├─────────────────────────────")
        
        send_formatted_message(
            bot,
            chat_id,
            "📊 График эскалаций Hybris",
            lines[:-1]  # Убираем последний разделитель
        )
        
    except Exception as e:
        logger.error(f"Error showing Hybris schedule: {e}")
        send_error_message(
            bot,
            chat_id,
            "Ошибка при загрузке графика Hybris",
            reply_markup=create_main_menu()
        )

@log_action("Current Hybris week viewed")
def show_current_hybris_week(bot, chat_id):
    """Показывает текущую неделю Hybris"""
    try:
        df = load_hybris_schedule()
        if df is None or df.empty:
            return send_error_message(
                bot,
                chat_id,
                "Не удалось загрузить график Hybris",
                reply_markup=create_main_menu()
            )
        
        current_date = datetime.now()
        
        # Ищем текущую неделю
        current_week = None
        for _, row in df.iterrows():
            week_range = row["Неделя"]
            if pd.notna(week_range) and " - " in str(week_range):
                start_str = str(week_range).split(" - ")[0]
                try:
                    start_date = datetime.strptime(start_str.split()[0], "%d.%m")
                    # Устанавливаем текущий год для сравнения
                    start_date = start_date.replace(year=current_date.year)
                    
                    if start_date <= current_date:
                        current_week = row
                except ValueError:
                    continue
        
        if current_week is None:
            return send_error_message(
                bot,
                chat_id,
                "Не найдена текущая неделя в графике Hybris",
                reply_markup=create_main_menu()
            )
        
        week = current_week["Неделя"] if pd.notna(current_week["Неделя"]) else "Текущая неделя"
        first_esc = current_week["Первая эскалация"] if pd.notna(current_week["Первая эскалация"]) else "—"
        second_esc = current_week["Вторая эскалация"] if pd.notna(current_week["Вторая эскалация"]) else "—"
        
        lines = [
            f"│ <b>📅 Неделя</b>: {week}",
            f"│ <b>👑 1-я эскалация</b>: {first_esc}",
            f"│ <b>🔹 2-я эскалация</b>: {second_esc}"
        ]
        
        send_formatted_message(
            bot,
            chat_id,
            "📊 Текущая неделя Hybris",
            lines
        )
        
    except Exception as e:
        logger.error(f"Error showing current Hybris week: {e}")
        send_error_message(
            bot,
            chat_id,
            "Ошибка при загрузке текущей недели Hybris",
            reply_markup=create_main_menu()
        )

def load_hybris_schedule():
    """Загружает график Hybris из Excel"""
    try:
        # Исправляем путь к файлу - используем Config из storage
        from config import Config
        df = pd.read_excel(Config.SCHEDULE_FILE, sheet_name="Hybris")
        return df
    except Exception as e:
        logger.error(f"Error loading Hybris schedule: {e}")
        return None