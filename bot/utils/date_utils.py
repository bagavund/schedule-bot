from datetime import datetime

def parse_date(date_str):
    try:
        if '.' in date_str and len(date_str.split('.')) == 2:
            date_str = f"{date_str}.{datetime.now().year}"
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        return None