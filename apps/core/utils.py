from datetime import timedelta
from django.utils import timezone


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def today():
    return timezone.localtime(timezone.now()).date()
