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
    
    # Добавляем оба варианта имени для совместимости
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    BOT_TOKEN = TELEGRAM_TOKEN  # Алиас для обратной совместимости
    
    if not TELEGRAM_TOKEN:
        raise ValueError("Токен бота не найден в .env файле")
    
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
                "Отсутствуют необходимые файлы:\n" + "\n".join(missing_files))