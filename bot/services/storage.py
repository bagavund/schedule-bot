import pandas as pd
from functools import lru_cache
from config import Config


@lru_cache(maxsize=1)
def load_schedule():
    try:
        df = pd.read_excel(Config.SCHEDULE_FILE, sheet_name="Лист2")
        df["Дата"] = pd.to_datetime(df["Дата"]).dt.date
        if "Резерв" not in df.columns:
            df["Резерв"] = pd.NA
        if "Руководитель" not in df.columns:
            df["Руководитель"] = pd.NA
        return df
    except Exception as e:
        print(f"Ошибка загрузки файла расписания: {e}")
        return None


def load_allowed_users():
    try:
        with open(Config.ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"Ошибка загрузки списка пользователей: {e}")
        return []
