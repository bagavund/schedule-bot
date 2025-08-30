from datetime import datetime, timedelta
from bot.services import auth, schedule
from bot.keyboards import create_main_menu
from bot.utils.schedule_utils import with_schedule
from bot.utils import (
    log_action,
    send_formatted_message,
    send_error_message,
    parse_date
)

@log_action("Schedule viewed")
@with_schedule
def show_schedule(bot, chat_id, date, df=None):
    """Показывает расписание ГСМАиЦП на указанную дату"""
    if df is None:
        send_error_message(
            bot,
            chat_id,
            "⚠️ Не удалось загрузить расписание",
            reply_markup=create_main_menu()
        )
        return
        
    schedule_data = schedule.get_date_schedule(df, date)
    if schedule_data is not None:
        send_formatted_message(
            bot,
            chat_id,
            f"📊 ГСМАиЦП на {date.strftime('%d.%m.%Y')}",
            schedule.format_schedule(schedule_data).split('\n')[2:-1],
            reply_markup=create_main_menu()
        )
    else:
        if df.empty:
            send_error_message(
                bot,
                chat_id,
                "Файл расписания пуст или не загружен",
                reply_markup=create_main_menu()
            )
        else:
            min_date = df["Дата"].min()
            max_date = df["Дата"].max()
            send_error_message(
                bot,
                chat_id,
                f"Расписание на {date.strftime('%d.%m.%Y')} не найдено.\n"
                f"Доступный диапазон: {min_date.strftime('%d.%m.%Y')} - {max_date.strftime('%d.%m.%Y')}",
                reply_markup=create_main_menu()
            )

def handle_gsma_today(bot, message):
    """Обработчик для кнопки 'Сегодня ГСМА'"""
    show_schedule(bot, message.chat.id, datetime.now().date())

def handle_gsma_tomorrow(bot, message):
    """Обработчик для кнопки 'Завтра ГСМА'"""
    show_schedule(bot, message.chat.id, datetime.now().date() + timedelta(days=1))

def request_gsma_date(bot, chat_id):
    """Запрос даты для графика ГСМАиЦП"""
    msg = bot.send_message(
        chat_id,
        "📅 Введите дату в формате ДД.ММ (например, 25.07):",
        parse_mode="HTML",
    )
    bot.register_next_step_handler(msg, lambda m: process_gsma_date_input(bot, m))

def process_gsma_date_input(bot, message):
    """Обработка введенной даты для графика ГСМАиЦП"""
    chat_id = message.chat.id
    date_obj = parse_date(message.text)
    
    if date_obj:
        show_schedule(bot, chat_id, date_obj)
    else:
        send_error_message(
            bot,
            chat_id,
            "Неверный формат даты. Введите дату в формате ДД.ММ (например, 25.07).",
            reply_markup=create_main_menu()
        )