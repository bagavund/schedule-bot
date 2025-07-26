from telebot import types

def send_formatted_message(bot, chat_id, header, lines, reply_markup=None):
    message = [f"<b>{header}</b>", "<pre>┌─────────────────────────────"]
    message.extend(lines)
    message.append("└─────────────────────────────</pre>")
    bot.send_message(chat_id, "\n".join(message), 
                    parse_mode="HTML", 
                    reply_markup=reply_markup)

def send_error_message(bot, chat_id, text, reply_markup=None):
    bot.send_message(chat_id, f"⚠️ {text}", 
                    parse_mode="HTML",
                    reply_markup=reply_markup)