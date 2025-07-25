# 📅 Schedule Bot | Бот для проверки графика дежурств

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-green.svg)

## 🌟 Основные функции

### Для сотрудников
- Просмотр своих смен (`Мои смены`)
- Уведомления о ближайшей смене
- Статистика отработанных часов
- Поиск смен на конкретную дату

### Для администраторов
- Авторизация по списку разрешенных пользователей
- Логирование всех действий

## 🛠 Технологии

- Python 3.13+
- `python-telegram-bot`
- Pandas (для работы с Excel)
- Логирование в файлы

## ⚙️ Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-репозиторий/schedule-bot.git
cd schedule-bot
```
2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Настройте конфигурацию:
```bash
cp .env.example .env
nano .env  # Отредактируйте файл
```

# 🔐 Настройка доступа
Добавьте пользователей в data/allowed_users.txt:

```text
Иванов Иван
Петров Петр
```
Настройте файл расписания (data/расписание.xlsx) с колонками:
```
Дата
Основа (основной сотрудник)
Ночь (ночная смена)
Администрирование
Резерв
```

# 📊 Логирование
Система логирования сохраняет:

Все действия пользователей

Ошибки и предупреждения

Попытки доступа

Логи хранятся в data/logs/ в формате:

text
user_activity_YYYY-MM.log
