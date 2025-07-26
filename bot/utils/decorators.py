from bot.services.user_logging import user_activity_logger
from bot.services import auth

def get_chat_id_from_args(*args, **kwargs):
    for arg in args:
        if hasattr(arg, 'chat') and hasattr(arg.chat, 'id'):
            return arg.chat.id
    return kwargs.get('chat_id')

def log_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            chat_id = get_chat_id_from_args(*args, **kwargs)
            user_name = auth.get_user_name(chat_id) if chat_id else "Unknown"
            
            details = ""
            for arg in args:
                if hasattr(arg, 'text'):
                    details = f"Text: {arg.text[:100]}"
                    break
            
            user_activity_logger.log_activity(
                user_id=chat_id,
                username=user_name,
                action=action_name,
                details=details
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator