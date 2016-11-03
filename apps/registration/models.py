from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    LANGUAGE_CHOICES = (
        ('Japanese', 'Japanese'),
    )
    language_text = models.CharField(max_length=30, unique=True)


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    language = models.ForeignKey(Language)
    age = models.SmallIntegerField()
