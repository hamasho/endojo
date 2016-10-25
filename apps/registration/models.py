from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    language_text = models.CharField(max_length=30)


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    language = models.ForeignKey(Language)
    age = models.SmallIntegerField(null=True)
