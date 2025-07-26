from telebot import types
import logging
from bot.services import auth
from bot.keyboards import create_admin_keyboard, create_main_menu
from bot.utils.broadcast import BroadcastManager
from bot.utils.decorators import log_action

logger = logging.getLogger(__name__)

@log_action("Admin panel accessed")
def handle_admin_panel(bot, message):
    """Обработчик команды админ-панели"""
    if not auth.is_admin(message.chat.id):
        logger.warning(f"Unauthorized admin access attempt by {message.chat.id}")
        bot.send_message(message.chat.id, "⛔ Доступ запрещен")
        return
    
    bot.send_message(
        message.chat.id,
        "🛠 Панель администратора",
        reply_markup=create_admin_keyboard()
    )

@log_action("Broadcast initiated")
def handle_broadcast_start(bot, message):
    """Начало процесса рассылки"""
    msg = bot.send_message(
        message.chat.id,
        "📝 Введите сообщение для рассылки (поддерживается HTML-разметка):\n"
        "Напишите 'отмена' для отмены",
        reply_markup=types.ForceReply()
    )
    bot.register_next_step_handler(msg, lambda m: process_broadcast_message(bot, m))

def process_broadcast_message(bot, message):
    """Обработка сообщения для рассылки"""
    if message.text.lower() == 'отмена':
        return handle_admin_panel(bot, message)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_{message.id}"),
        types.InlineKeyboardButton("❌ Отменить", callback_data="cancel")
    )
    
    preview = bot.send_message(
        message.chat.id,
        f"✉️ Подтвердите рассылку:\n\n{message.text}",
        reply_markup=markup,
        parse_mode="HTML"
    )

def setup_admin_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_'))
    def confirm_broadcast(call):
        try:
            # Получаем текст из текущего сообщения, а не из reply_to_message
            message_text = call.message.text.split("Подтвердите рассылку:")[-1].strip()
            
            bot.edit_message_text(
                "🔄 Рассылка начата...",
                call.message.chat.id,
                call.message.id
            )
            
            broadcaster = BroadcastManager(bot)
            stats = broadcaster.broadcast_with_progress(message_text)
            
            bot.edit_message_text(
                f"✅ Рассылка завершена\nУспешно: {stats['success']}\nОшибки: {stats['failed']}",
                call.message.chat.id,
                call.message.id
            )
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
            bot.answer_callback_query(call.id, "❌ Ошибка при рассылке")
    
    @bot.callback_query_handler(func=lambda call: call.data == 'cancel')
    def cancel_broadcast(call):
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "❌ Рассылка отменена")

__all__ = [
    'handle_admin_panel',
    'handle_broadcast_start',
    'setup_admin_handlers'
]