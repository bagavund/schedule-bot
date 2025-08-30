import logging
import time
from bot.services.auth import user_states
from bot.utils import log_action, send_error_message

logger = logging.getLogger(__name__)

@log_action("Broadcast requested")
def handle_broadcast(bot, message):
    """Обработчик рассылки сообщений"""
    chat_id = message.chat.id
    
    from bot.services.auth import is_admin_user
    if not is_admin_user(chat_id):
        send_error_message(bot, chat_id, "❌ Эта команда доступна только администратору.")
        return
    
    broadcast_text = message.text.replace('/broadcast', '').strip()
    
    if not broadcast_text:
        send_error_message(bot, chat_id, "❌ Укажите сообщение для рассылки.\n\nПример: /broadcast Завтра собрание в 10:00")
        return
    
    recipients = []
    
    for user_chat_id, user_info in user_states.items():
        if user_info.get('authorized'):
            recipients.append({
                'chat_id': user_chat_id,
                'name': user_info.get('name', 'Unknown')
            })
    
    if not recipients:
        send_error_message(bot, chat_id, "❌ Нет авторизованных пользователей для рассылки.")
        return
    
    process_broadcast(bot, chat_id, broadcast_text, recipients)

def process_broadcast(bot, admin_chat_id, broadcast_text, recipients):
    """Выполняет рассылку сообщения"""
    success_count = 0
    fail_count = 0
    
    status_message = bot.send_message(
        admin_chat_id,
        f"⏳ <b>Начинаю рассылку...</b>\n\nПолучателей: {len(recipients)}",
        parse_mode="HTML"
    )
    
    for i, recipient in enumerate(recipients, 1):
        if send_to_user(bot, recipient['chat_id'], broadcast_text, recipient['name']):
            success_count += 1
        else:
            fail_count += 1

        if i % 10 == 0:
            try:
                bot.edit_message_text(
                    f"⏳ <b>Рассылка в процессе...</b>\n\nОтправлено: {i}/{len(recipients)}",
                    admin_chat_id,
                    status_message.message_id,
                    parse_mode="HTML"
                )
            except:
                pass
        time.sleep(0.1)
    
    # Финальный статус
    bot.edit_message_text(
        f"✅ <b>Рассылка завершена!</b>\n\n"
        f"Успешно: {success_count}\n"
        f"Не удалось: {fail_count}\n"
        f"Всего: {len(recipients)}",
        admin_chat_id,
        status_message.message_id,
        parse_mode="HTML"
    )

def send_to_user(bot, user_chat_id, message_text, user_name=None):
    """Отправка сообщения конкретному пользователю"""
    try:
        text = f"📢 <b>Уведомление от администратора</b>\n\n{message_text}"
        bot.send_message(user_chat_id, text, parse_mode="HTML")
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки пользователю {user_chat_id}: {e}")
        return False