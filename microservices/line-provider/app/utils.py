from datetime import timedelta, datetime


def get_deadline_seconds(now: datetime, deadline: datetime) -> timedelta:
    return deadline - now
