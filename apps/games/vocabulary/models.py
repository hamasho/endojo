from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from registration.models import Language


class Package(models.Model):
    title = models.CharField(max_length=200, unique=True)
    level = models.SmallIntegerField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-pub_date']


class Word(models.Model):
    word_text = models.CharField(max_length=40, unique=True)
    package = models.ForeignKey(Package)


class TranslatedWord(models.Model):
    word = models.ForeignKey(Word)
    language = models.ForeignKey(Language)
    meaning = models.CharField(max_length=100)


class WordState(models.Model):
    """
    Class for memorizing state of word.

    `state` column indicates how deeply the user remember the word.
    This value can be 1 to 6, and each indicates the span
    from `last_appeared` until next vocabulary game.
    1: 1 day
    2: 2 days
    3: 4 days
    4: 1 week
    5: 2 weeks
    6: 3 weeks
    If the user can answer the meanigs of word with which state is 6,
    it is marked remembered and the word disappears from this model.
    """
    state = models.SmallIntegerField(default=1)
    user = models.ForeignKey(User)
    word = models.ForeignKey(Word)
    last_appeared = models.DateField(auto_now=True)


class ClearedPackage(models.Model):
    package = models.ForeignKey(Package)
    user = models.ForeignKey(User)
    cleared_date = models.DateTimeField(default=timezone.now)
