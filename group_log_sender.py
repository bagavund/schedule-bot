#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/group_log_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GroupLogSender:
    def __init__(self):
        self.bot_token = "8240720669:AAHfORT0ji75iKWNW3XPz9WT8jcFeIESt1Y"
        self.group_id = "-4875103348"  # ID группы "логи"
        self.log_file = Path("/root/schedule-bot/data/logs/user_activity_2025-08.log")
        self.sent_position = 0
        
        # Создаем директорию для логов если нет
        self.log_file.parent.mkdir(exist_ok=True)
        
        logger.info("Инициализация GroupLogSender для группы")
        logger.info(f"Мониторим файл: {self.log_file}")
        
    def send_to_group(self, message):
        """Отправляет сообщение в группу"""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.group_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_notification": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.json().get("ok"):
                logger.info("Сообщение отправлено в группу")
                return True
            else:
                error = response.json().get('description', 'Unknown error')
                logger.error(f"Ошибка API Telegram: {error}")
                return False
        except Exception as e:
            logger.error(f"Ошибка отправки: {e}")
            return False
    
    def monitor_logs(self):
        """Мониторит логи и отправляет в группу"""
        logger.info("Запуск мониторинга логов...")
        
        while True:
            try:
                if self.log_file.exists():
                    current_size = self.log_file.stat().st_size
                    
                    # Если файл перезаписан (log rotation)
                    if current_size < self.sent_position:
                        self.sent_position = 0
                        logger.warning("Обнаружен log rotation, сбрасываем позицию")
                    
                    if current_size > self.sent_position:
                        # Читаем новые строки
                        with open(self.log_file, 'r', encoding='utf-8') as f:
                            f.seek(self.sent_position)
                            new_lines = f.readlines()
                            
                        if new_lines:
                            # Форматируем сообщение для группы
                            message = "Новая активность в системе:\n\n"
                            
                            for line in new_lines:
                                line = line.strip()
                                if line:  # Пропускаем пустые строки
                                    message += f"{line}\n"
                            
                            # Обрезаем если слишком длинное
                            if len(message) > 4000:
                                message = message[:4000] + "..."
                            
                            # Отправляем в группу
                            if self.send_to_group(message):
                                logger.info(f"Отправлено {len(new_lines)} строк в группу")
                                self.sent_position = current_size
                            else:
                                logger.error("Не удалось отправить сообщение в группу")
                
                time.sleep(10)  # Проверка каждые 10 секунд
                
            except FileNotFoundError:
                logger.warning("Файл логов не найден, ждем...")
                time.sleep(30)
            except Exception as e:
                logger.error(f"Ошибка мониторинга: {e}")
                time.sleep(30)

if __name__ == "__main__":
    try:
        sender = GroupLogSender()
        sender.monitor_logs()
    except KeyboardInterrupt:
        logger.info("Остановка по запросу пользователя")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
