import time
import logging
from telebot import TeleBot
from bot.services import auth
from tqdm import tqdm

logger = logging.getLogger(__name__)

class BroadcastManager:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.delay = 0.3

    def get_active_users(self):
        return [int(chat_id) for chat_id in auth.user_states if auth.is_authorized(chat_id)]

    def send_broadcast(self, text: str, max_retries: int = 2) -> dict:
        users = self.get_active_users()
        stats = {'success': 0, 'failed': 0, 'errors': {}}
        
        for chat_id in users:
            for attempt in range(max_retries):
                try:
                    self.bot.send_message(
                        chat_id=chat_id,
                        text=text,
                        parse_mode="HTML"
                    )
                    stats['success'] += 1
                    time.sleep(self.delay)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        stats['failed'] += 1
                        stats['errors'][str(chat_id)] = str(e)
                        logger.error(f"Broadcast error for {chat_id}: {e}")
        
        return stats

    def broadcast_with_progress(self, text: str):
        users = self.get_active_users()
        with tqdm(total=len(users), desc="Broadcasting") as pbar:
            stats = self.send_broadcast(text)
            pbar.update(len(users))
        return stats