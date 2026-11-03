from datetime import datetime, timedelta
from typing import Callable


def calc_period_growth(current: int, previous: int) -> float:
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round((current - previous) / previous * 100, 1)


def build_time_series(
    db,
    count_func: Callable[[datetime, datetime], int],
    days: int
) -> tuple[list[str], list[int]]:
    now = datetime.now()
    labels = []
    values = []

    days = min(days, 30)
    for i in range(days, -1, -1):
        start = now - timedelta(days=i + 1)
        end = now - timedelta(days=i)
        count = count_func(start, end)
        labels.append(start.strftime("%m-%d"))
        values.append(count)

    return labels, values
