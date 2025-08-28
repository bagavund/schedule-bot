import json
import os
import logging
from datetime import datetime
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)

# Пути к файлам
DATA_DIR = Config.DATA_DIR
USER_STATES_FILE = DATA_DIR / "user_states.json"

# Создаем директорию, если не существует
os.makedirs(DATA_DIR, exist_ok=True)

# Глобальные переменные
user_states = {}
ADMIN_USER = "Комлев Владислав"

def load_user_states():
    """Загружает состояния пользователей из файла"""
    global user_states
    try:
        if USER_STATES_FILE.exists():
            with open(USER_STATES_FILE, "r", encoding="utf-8") as f:
                user_states = json.load(f)
        else:
            user_states = {}
            save_user_states()
    except Exception as e:
        logger.error(f"Ошибка загрузки user_states: {e}")
        user_states = {}

def save_user_states():
    """Сохраняет состояния пользователей в файл"""
    try:
        with open(USER_STATES_FILE, "w", encoding="utf-8") as f:
            json.dump(user_states, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения user_states: {e}")

def is_authorized(chat_id):
    """Проверяет авторизацию пользователя"""
    return str(chat_id) in user_states and user_states[str(chat_id)].get("authorized", False)

def get_user_name(chat_id):
    """Возвращает имя пользователя"""
    return user_states.get(str(chat_id), {}).get("name")

def get_current_user(chat_id):
    """Возвращает полную информацию о текущем пользователе"""
    return user_states.get(str(chat_id), {})

def is_admin_user(chat_id):
    """Проверяет, является ли пользователь администратором"""
    user_info = get_current_user(chat_id)
    return user_info.get("name") == ADMIN_USER or user_info.get("original_name") == ADMIN_USER

def authorize_user_by_username(message, full_name_input):
    """Авторизация по логину Telegram и ФИО"""
    from .storage import load_allowed_users, load_allowed_users_fallback
    
    # Получаем логин пользователя (если есть)
    username = f"@{message.from_user.username.lower()}" if message.from_user.username else None
    chat_id = str(message.chat.id)
    
    allowed_users = load_allowed_users()
    
    # Сценарий 1: Пользователь имеет username
    if username:
        # Проверка 1: Логин должен быть в списке разрешенных
        if username not in allowed_users:
            return False, f"❌ Логин {username} не найден в списке разрешенных.\n\nОбратитесь к администратору для добавления в систему."

        # Проверка 2: ФИО должно совпадать с записью
        expected_full_name = allowed_users[username]
        if expected_full_name != full_name_input:
            return False, f"❌ Неверные данные. Ожидается: {expected_full_name}\n\nВведите правильные фамилию и имя:"

        # Успешная авторизация
        user_info = {
            "authorized": True, 
            "name": expected_full_name,
            "username": username,
            "chat_id": chat_id,
            "authorized_at": datetime.now().isoformat(),
            "auth_method": "username"
        }
        
        user_states[chat_id] = user_info
        save_user_states()
        
        logger.info(f"User authorized by username: {expected_full_name} ({username})")
        return True, f"✅ Авторизация успешна, {expected_full_name}!"
    
    # Сценарий 2: Пользователь без username - используем fallback
    else:
        fallback_users = load_allowed_users_fallback()
        
        # Проверка: chat_id должен быть в резервном списке
        if chat_id not in fallback_users:
            return False, "❌ У вашего аккаунта Telegram не установлен username (@логин).\n\nОбратитесь к администратору для альтернативного способа доступа."

        # Проверка: ФИО должно совпадать
        expected_full_name = fallback_users[chat_id]
        if expected_full_name != full_name_input:
            return False, f"❌ Неверные данные. Ожидается: {expected_full_name}\n\nВведите правильные фамилию и имя:"

        # Успешная авторизация через fallback
        user_info = {
            "authorized": True, 
            "name": expected_full_name,
            "username": None,
            "chat_id": chat_id,
            "authorized_at": datetime.now().isoformat(),
            "auth_method": "fallback"
        }
        
        user_states[chat_id] = user_info
        save_user_states()
        
        logger.info(f"User authorized by fallback: {expected_full_name} (ID: {chat_id})")
        return True, f"✅ Авторизация успешна, {expected_full_name}!"

def authorize_user_legacy(chat_id, full_name_input):
    """Функция для имперсонации администратора - работает с новым форматом"""
    from .storage import load_allowed_users
    
    allowed_users = load_allowed_users()  # Новый формат: @логин:ФИО
    
    # Ищем ФИО в значениях (в новом формате значения - это ФИО)
    found = False
    expected_full_name = None
    
    for username, full_name in allowed_users.items():
        if full_name == full_name_input:
            found = True
            expected_full_name = full_name
            break
    
    if not found:
        return False, "❌ Неверные данные. Пользователь не найден в списке разрешенных."

    # Для администратора пропускаем дополнительные проверки
    current_user_info = get_current_user(chat_id)
    is_currently_admin = current_user_info.get("name") == ADMIN_USER or current_user_info.get("original_name") == ADMIN_USER

    if is_currently_admin:
        user_info = {
            "authorized": True, 
            "name": expected_full_name,
            "chat_id": str(chat_id),
            "original_name": ADMIN_USER,
            "is_impersonating": True,
            "auth_method": "admin_impersonation"
        }
        user_states[str(chat_id)] = user_info
        save_user_states()
        logger.info(f"Admin impersonating user: {expected_full_name}")
        return True, f"✅ Переключение на {expected_full_name} успешно!"

    return False, "❌ Устаревший метод авторизации. Используйте новый формат."

def deauthorize_user(chat_id):
    """Деавторизует пользователя"""
    chat_id = str(chat_id)
    if chat_id in user_states:
        # Если это была имперсонация администратора, возвращаем к оригинальному пользователю
        user_info = user_states[chat_id]
        if user_info.get("is_impersonating") and user_info.get("original_name") == ADMIN_USER:
            user_states[chat_id] = {
                "authorized": True,
                "name": ADMIN_USER,
                "chat_id": chat_id,
                "auth_method": "admin_revert"
            }
            save_user_states()
            logger.info(f"Admin stopped impersonation: {ADMIN_USER}")
        else:
            del user_states[chat_id]
            save_user_states()
            logger.info(f"User deauthorized (ID: {chat_id})")

load_user_states()
logger.info(f"Модуль auth инициализирован. Загружено {len(user_states)} пользователей")