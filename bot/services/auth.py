import json
import os
import logging
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

def load_allowed_users():
    """Загружает список разрешенных пользователей"""
    try:
        with open(Config.ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Ошибка загрузки разрешенных пользователей: {e}")
        return []

def is_authorized(chat_id):
    """Проверяет авторизацию пользователя"""
    return str(chat_id) in user_states and user_states[str(chat_id)].get("authorized", False)

def get_user_name(chat_id):
    """Возвращает имя пользователя"""
    return user_states.get(str(chat_id), {}).get("name")

def authorize_user(chat_id, full_name):
    """Авторизует пользователя"""
    allowed_users = load_allowed_users()
    
    if not allowed_users:
        logger.error("Список разрешенных пользователей пуст")
        return False, "❌ Ошибка: файл с разрешёнными пользователями не найден или пуст"

    if full_name in allowed_users:
        user_states[str(chat_id)] = {"authorized": True, "name": full_name}
        save_user_states()
        logger.info(f"Пользователь авторизован: {full_name} (ID: {chat_id})")
        return True, f"✅ Авторизация успешна, {full_name}!"
    
    logger.warning(f"Попытка авторизации неразрешенного пользователя: {full_name}")
    return False, "❌ Неверные данные. Попробуйте ещё раз:"

def deauthorize_user(chat_id):
    """Деавторизует пользователя"""
    chat_id = str(chat_id)
    if chat_id in user_states:
        del user_states[chat_id]
        save_user_states()
        logger.info(f"Пользователь деавторизован (ID: {chat_id})")

# Инициализация при загрузке модуля
load_user_states()
logger.info(f"Модуль auth инициализирован. Загружено {len(user_states)} пользователей")