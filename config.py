import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

class Config:
    PROJECT_ROOT = Path(__file__).parent
    DATA_DIR = PROJECT_ROOT / "data"
    LOGS_DIR = DATA_DIR / "logs"
    
    SCHEDULE_FILE = DATA_DIR / "расписание.xlsx"
    ALLOWED_USERS_FILE = DATA_DIR / "allowed_users.txt"
    USER_STATES_FILE = DATA_DIR / "user_states.json"
    ADMINS_FILE = DATA_DIR / "admins.txt"  # Новый файл
    
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    @classmethod
    def load_admins(cls):
        try:
            with open(cls.ADMINS_FILE, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    @classmethod
    def verify_files_exist(cls):
        """Проверяет существование необходимых файлов"""
        required_files = {
            "Файл расписания": cls.SCHEDULE_FILE,
            "Файл разрешенных пользователей": cls.ALLOWED_USERS_FILE,
        }

        missing_files = []
        for name, path in required_files.items():
            if not path.exists():
                missing_files.append(f"{name} не найден: {path}")

        if missing_files:
            raise FileNotFoundError(
                "Отсутствуют необходимые файлы:\n" + "\n".join(missing_files)
            )
