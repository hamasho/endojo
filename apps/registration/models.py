from datetime import date
from django.db import models
from django.contrib.auth.models import User


def calculate_age(born):
    today = date.today()
    years_difference = today.year - born.year
    is_before_birthday = (today.month, today.day) < (born.month, born.day)
    elapsed_years = years_difference - int(is_before_birthday)
    return elapsed_years


class Language(models.Model):
    JAPANESE = 'ja'
    LANGUAGE_CHOICES = (
        (JAPANESE, 'Japanese'),
    )
    language_text = models.CharField(
        max_length=30, choices=LANGUAGE_CHOICES, unique=True)


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    language = models.ForeignKey(Language)
    birth_date = models.DateField()

    def age(self):
        return calculate_age(self.birth_date)
