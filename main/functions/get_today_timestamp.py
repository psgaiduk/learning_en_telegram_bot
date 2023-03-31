from datetime import datetime


def get_today_timestamp():
    """Get today by timestamp."""
    return datetime.utcnow().replace(hour=0, minute=0, second=0).timestamp()
