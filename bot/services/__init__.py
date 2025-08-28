from .auth import (
    is_authorized, 
    authorize_user_by_username,  # ← Изменено с authorize_user
    authorize_user_legacy,       # ← Добавлено для обратной совместимости
    get_user_name, 
    deauthorize_user,
    is_admin_user,
    get_current_user
)
from .user_logging import user_activity_logger
from .schedule import (
    format_schedule,
    get_date_schedule,
    get_user_shifts,
    WEEKDAYS,
    SHIFT_DURATIONS,
)
from .storage import load_schedule, load_allowed_users, load_allowed_users_fallback  # ← Добавлены новые функции

__all__ = [
    "is_authorized",
    "authorize_user_by_username",  # ← Изменено
    "authorize_user_legacy",       # ← Добавлено
    "get_user_name",
    "deauthorize_user",
    "is_admin_user",
    "get_current_user",
    "format_schedule",
    "get_date_schedule",
    "get_user_shifts",
    "load_schedule",
    "load_allowed_users",
    "load_allowed_users_fallback",  # ← Добавлено
    "WEEKDAYS",
    "SHIFT_DURATIONS",
    "user_activity_logger",
]