# Schedule Bot

Telegram-бот для проверки графика работы. 

## Установка и запуск

### Требования
- Python 3.13+
- Telegram Bot API Token
- Ubuntu server

 ### Клонирование репозитория
```bash
git clone https://github.com/bagavund/schedule-bot.git
cd schedule-bot
```

### Настройка окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Дополнительные файлы

```bash
mkdir allowed_users.txt
mkdir расписание.xlsx
touch .env
```

#### data/allowed_users.txt
Вносится фамилия и имя как в графике (например Иванов Иван)

#### data/расписание.xlsx
Пока что поддерживается только такой формат Excel таблицы:

```
   Дата        Основа      Администрирование        Ночь          Резерв          Отпуск
01.01.2025   Работник 1       Работник 2         Работник 3     Работник 4      Работник 4
02.01.2025   Работник 1       Работник 2         Работник 3     Работник 4      Работник 4
```
#### .env
```
TELEGRAM_BOT_TOKEN=токен_из_@BotFather
```
