import pandas as pd
from functools import lru_cache
import logging
from config import Config

logger = logging.getLogger(__name__)

@lru_cache(maxsize=2)
def load_schedule(sheet_name="ГСМАиЦП"):
    """Загружает расписание с указанного листа"""
    try:
        df = pd.read_excel(Config.SCHEDULE_FILE, sheet_name=sheet_name)
        
        if sheet_name == "ГСМАиЦП":
            df["Дата"] = pd.to_datetime(df["Дата"]).dt.date
            for col in ["Резерв", "Руководитель", "Ведущий специалист"]: 
                if col not in df.columns:
                    df[col] = pd.NA
        
        return df
    except Exception as e:
        logger.error(f"Error loading schedule from {sheet_name}: {e}", exc_info=True)
        return None

def load_allowed_users():
    """Загружает список разрешенных пользователей с логинами Telegram"""
    try:
        allowed_users = {}
        with open(Config.ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                username, full_name = line.split(':', 1)
                allowed_users[username.strip().lower()] = full_name.strip()
        
        return allowed_users
    except Exception as e:
        logger.error(f"Error loading allowed users: {e}", exc_info=True)
        return {}

def load_allowed_users_fallback():
    """Загружает резервный список пользователей без username (по chat_id)"""
    try:
        allowed_users = {}
        fallback_file = Config.DATA_DIR / "allowed_users_fallback.txt"
        
        if fallback_file.exists():
            with open(fallback_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                    
                    chat_id, full_name = line.split(':', 1)
                    allowed_users[chat_id.strip()] = full_name.strip()
        
        return allowed_users
    except Exception as e:
        logger.error(f"Error loading fallback users: {e}")
        return {}

def load_allowed_users_legacy():
    """Загружает старый формат списка пользователей (для обратной совместимости)"""
    try:
        allowed_users = {}
        with open(Config.ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Старый формат: ФИО:ID или просто ФИО
                if ':' in line:
                    name, telegram_id = line.split(':', 1)
                    allowed_users[name.strip()] = telegram_id.strip()
                else:
                    allowed_users[line.strip()] = None
        
        return allowed_users
    except Exception as e:
        logger.error(f"Error loading legacy allowed users: {e}")
        return {}