import json
from pathlib import Path
import os
from bot.services.storage import load_allowed_users

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
USER_STATES_FILE = DATA_DIR / "user_states.json"

os.makedirs(DATA_DIR, exist_ok=True)

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
    except (json.JSONDecodeError, PermissionError, OSError) as e:
        print(f"Ошибка загрузки user_states: {e}")
        user_states = {}


def save_user_states():
    """Сохраняет состояния пользователей в файл"""
    try:
        with open(USER_STATES_FILE, "w", encoding="utf-8") as f:
            json.dump(user_states, f, ensure_ascii=False, indent=2)
    except (PermissionError, OSError) as e:
        print(f"Ошибка сохранения user_states: {e}")


def is_authorized(chat_id):
    """Проверяет авторизацию пользователя"""
    return str(chat_id) in user_states and user_states[str(chat_id)].get(
        "authorized", False
    )


def get_user_name(chat_id):
    """Возвращает имя пользователя"""
    return user_states.get(str(chat_id), {}).get("name")


def authorize_user(chat_id, full_name):
    """Авторизует пользователя"""
    allowed_users = load_allowed_users()

    if not allowed_users:
        return False, "❌ Ошибка: файл с разрешёнными пользователями не найден или пуст"

    if full_name in allowed_users:
        user_states[str(chat_id)] = {"authorized": True, "name": full_name}
        save_user_states()
        return True, f"✅ Авторизация успешна, {full_name}!"
    return False, "❌ Неверные данные. Попробуйте ещё раз:"


def deauthorize_user(chat_id):
    """Деавторизует пользователя"""
    chat_id = str(chat_id)
    if chat_id in user_states:
        del user_states[chat_id]
        save_user_states()


load_user_states()
