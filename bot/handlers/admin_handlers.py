from telebot import types
import logging
from bot.services import auth
from bot.keyboards import create_admin_keyboard, create_main_menu
from bot.utils.broadcast import BroadcastManager
from bot.utils.decorators import log_action

logger = logging.getLogger(__name__)

@log_action("Admin panel accessed")
def handle_admin_panel(bot, message):
    if not auth.is_admin(message.chat.id):
        logger.warning(f"Unauthorized admin access by {message.chat.id}")
        bot.send_message(
            message.chat.id,
            "⛔ Доступ запрещен",
            reply_markup=create_main_menu()
        )
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("📢 Рассылка"))
    markup.row(types.KeyboardButton("📊 Статистика"))
    markup.row(types.KeyboardButton("🔙 Выйти из админки"))
    
    bot.send_message(
        message.chat.id,
        "🛠 Панель администратора",
        reply_markup=markup
    )

@log_action("Broadcast initiated")
def handle_broadcast_start(bot, message):
    msg = bot.send_message(
        message.chat.id,
        "📝 Введите сообщение для рассылки:\n(Напишите 'отмена' для отмены)",
        reply_markup=types.ForceReply()
    )
    bot.register_next_step_handler(msg, lambda m: process_broadcast_message(bot, m))

def process_broadcast_message(bot, message):
    if message.text.lower() == 'отмена':
        return handle_admin_panel(bot, message)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_{message.id}"),
        types.InlineKeyboardButton("❌ Отменить", callback_data="cancel")
    )
    
    bot.send_message(
        message.chat.id,
        f"✉️ Подтвердите рассылку:\n\n{message.text}",
        reply_markup=markup
    )

def setup_admin_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_'))
    def confirm_broadcast(call):
        try:
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
            
            # Возврат в админ-панель
            handle_admin_panel(bot, call.message)
            
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
            bot.answer_callback_query(call.id, "❌ Ошибка при рассылке")
            handle_admin_panel(bot, call.message)

    @bot.callback_query_handler(func=lambda call: call.data == 'cancel')
    def cancel_broadcast(call):
        try:
            bot.delete_message(call.message.chat.id, call.message.id)
            handle_admin_panel(bot, call.message)
        except Exception as e:
            logger.error(f"Cancel error: {e}")
            bot.send_message(
                call.message.chat.id,
                "Ошибка при отмене",
                reply_markup=create_admin_keyboard()
            )

__all__ = [
    'handle_admin_panel',
    'handle_broadcast_start',
    'setup_admin_handlers'
]