import pandas as pd
from functools import lru_cache
import logging
from config import Config

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def load_schedule():
    try:
        df = pd.read_excel(Config.SCHEDULE_FILE, sheet_name="Лист2")
        df["Дата"] = pd.to_datetime(df["Дата"]).dt.date
        
        # Добавляем отсутствующие колонки
        for col in ["Резерв", "Руководитель"]:
            if col not in df.columns:
                df[col] = pd.NA
                
        return df
    except Exception as e:
        logger.error(f"Error loading schedule: {e}", exc_info=True)
        return None

def load_allowed_users():
    try:
        with open(Config.ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error loading allowed users: {e}", exc_info=True)
        return []