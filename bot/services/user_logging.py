import logging
from pathlib import Path
from datetime import datetime
from config import Config

class UserActivityLogger:
    def __init__(self):
        self.log_dir = Config.DATA_DIR / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f"user_activity_{datetime.now().strftime('%Y-%m')}.log"
        self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger("user_activity")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_activity(self, user_id, username, action, details=""):
        log_message = f"UserID: {user_id} | Username: {username} | Action: {action}"
        if details:
            log_message += f" | Details: {details}"
        self.logger.info(log_message)

user_activity_logger = UserActivityLogger()