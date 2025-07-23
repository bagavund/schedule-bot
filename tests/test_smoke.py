import sys
from pathlib import Path
import pytest

def test_imports():
    """Проверка импорта основных модулей"""
    project_root = str(Path(__file__).parent.parent)
    sys.path.insert(0, project_root)
    
    try:
        __import__('config') 
        __import__('bot.bot')
        __import__('bot.handlers')
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_config_loads():
    """Проверка загрузки конфигурации"""
    project_root = str(Path(__file__).parent.parent)
    sys.path.insert(0, project_root)
    
    try:
<<<<<<< HEAD
        from config import Config  # Импорт из корня
=======
        from config import Config 
>>>>>>> 26938504dac9c02c42658fde15dc0a93dbb9511f
        assert hasattr(Config, 'TELEGRAM_TOKEN')
    except ImportError as e:
        pytest.fail(f"Config import failed: {e}")
