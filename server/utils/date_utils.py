# server/date_utils.py
from datetime import datetime, timedelta
from typing import Optional


def get_current_datetime() -> datetime:
    """Returns the current date and time in UTC."""
    return datetime.utcnow()


def add_days_to_date(date: datetime, days: int) -> datetime:
    """Adds a specified number of days to a given date."""
    return date + timedelta(days=days)


def format_datetime(date: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Formats a datetime object into a string based on the given format."""
    return date.strftime(format)


def parse_datetime(
    date_str: str, format: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[datetime]:
    """Parses a string into a datetime object based on the given format."""
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        return None


def get_days_between_dates(start_date: datetime, end_date: datetime) -> int:
    """Returns the number of days between two dates."""
    delta = end_date - start_date
    return delta.days
