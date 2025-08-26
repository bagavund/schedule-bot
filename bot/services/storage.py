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
    try:
        with open(Config.ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Error loading allowed users: {e}", exc_info=True)
        return []