from datetime import timedelta
from django.utils import timezone


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def month_range(start_year, start_month, end_year, end_month):
    ym_start = 12 * start_year + start_month - 1
    ym_end = 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end + 1):
        y, m = divmod(ym, 12)
        yield y, m + 1


def get_today():
    return timezone.localtime(timezone.now()).date()
