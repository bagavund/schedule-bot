import sys
from pathlib import Path
import pytest

def test_imports():
    """Проверка импорта основных модулей"""
    # Добавляем корень проекта в PYTHONPATH
    project_root = str(Path(__file__).parent.parent)
    sys.path.insert(0, project_root)
    
    try:
        __import__('config')  # Импорт корневого config.py
        __import__('bot.bot')
        __import__('bot.handlers')
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_config_loads():
    """Проверка загрузки конфигурации"""
    project_root = str(Path(__file__).parent.parent)
    sys.path.insert(0, project_root)
    
    try:
        from config import Config  # Импорт из корня
        assert hasattr(Config, 'BOT_TOKEN')
    except ImportError as e:
        pytest.fail(f"Config import failed: {e}")