from datetime import datetime, timedelta
from bot.services import auth, schedule
from bot.keyboards import create_main_menu
from bot.utils.decorators import log_action
from bot.utils.schedule_utils import with_schedule
from bot.utils.response_utils import send_formatted_message, send_error_message
from bot.utils.date_utils import parse_date

@log_action("Schedule viewed")
@with_schedule
def show_schedule(bot, df, chat_id, date):
    schedule_data = schedule.get_date_schedule(df, date)
    if schedule_data is not None:
        send_formatted_message(
            bot,
            chat_id,
            f"📅 Расписание на {date.strftime('%d.%m.%Y')}",
            schedule.format_schedule(schedule_data).split('\n')[2:-1],
            reply_markup=create_main_menu()
        )
    else:
        send_error_message(
            bot,
            chat_id,
            f"На {date.strftime('%d.%m.%Y')} расписание не найдено.",
            reply_markup=create_main_menu()
        )

def handle_today(bot, message):
    show_schedule(bot, message.chat.id, datetime.now().date())

def handle_tomorrow(bot, message):
    show_schedule(bot, message.chat.id, datetime.now().date() + timedelta(days=1))

def request_date(bot, chat_id):
    msg = bot.send_message(
        chat_id,
        "📅 Введите дату в формате ДД.ММ (например, 25.07):",
        parse_mode="HTML",
    )
    bot.register_next_step_handler(msg, lambda m: process_date_input(bot, m))

def process_date_input(bot, message):
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