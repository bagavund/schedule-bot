import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / '.env')

class Config:
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError("Токен бота не найден в .env файле!")
    
    # Обновляем пути для работы в Docker
    DATA_DIR = Path('/app/data') if 'DOCKER' in os.environ else Path(__file__).parent / 'data'
    SCHEDULE_FILE = DATA_DIR / 'расписание.xlsx'
    ALLOWED_USERS_FILE = DATA_DIR / 'allowed_users.txt'