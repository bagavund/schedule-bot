import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / '.env')

class Config:
    # 1. Сначала определяем корневую директорию
    PROJECT_ROOT = Path(__file__).parent
    
    # 2. Затем определяем DATA_DIR
    DATA_DIR = PROJECT_ROOT / 'data'
    DATA_DIR.mkdir(exist_ok=True)  # Создаем папку, если ее нет
    
    # 3. Теперь можно определять файлы
    SCHEDULE_FILE = DATA_DIR / 'расписание.xlsx'
    ALLOWED_USERS_FILE = DATA_DIR / 'allowed_users.txt'
    USER_STATES_FILE = DATA_DIR / 'user_states.json'
    
    # 4. Затем токен бота (так как он может использовать предыдущие определения)
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError("Токен бота не найден в .env файле!")

    @classmethod
    def verify_files_exist(cls):
        """Проверяет существование необходимых файлов"""
        required_files = {
            'Файл расписания': cls.SCHEDULE_FILE,
            'Файл разрешенных пользователей': cls.ALLOWED_USERS_FILE
        }
        
        missing_files = []
        for name, path in required_files.items():
            if not path.exists():
                missing_files.append(f"{name} не найден: {path}")
        
        if missing_files:
            raise FileNotFoundError(
                "Отсутствуют необходимые файлы:\n" + 
                "\n".join(missing_files))
