import datetime
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

    @staticmethod
    def get_learning_words(user, count):
        pass


class AvailablePackage(models.Model):
    package = models.ForeignKey(Package)
    language = models.ForeignKey(Language)


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
    1: 0 day
    2: 1 days
    3: 3 days
    4: 1 week
    5: 2 weeks
    6: Mark as memorized
    If the user can answer the meanigs of word with which state is 6,
    it is marked remembered and the word disappears from this model.
    """
    state = models.SmallIntegerField(default=1)
    user = models.ForeignKey(User)
    word = models.ForeignKey(Word)
    last_appeared = models.DateField(auto_now=True)
    next_date = models.DateField(default=timezone.now)

    def level_up(self):
        self.state += 1
        if (self.state == 6):
            return

        if (self.state == 2):
            delta = datetime.timedelta(days=1)
        elif (self.state == 3):
            delta = datetime.timedelta(days=3)
        elif (self.state == 4):
            delta = datetime.timedelta(days=7)
        elif (self.state == 5):
            delta = datetime.timedelta(days=14)
        self.next_date = timezone.now() + delta

    def level_reset(self):
        self.state = 1

    def get_learning_words(user, count):
        result = []
        learning_words = WordState.objects.filter(
            user=user,
            state__lte=6,
            next_date__lte=timezone.now(),
        ).order_by('-state', '-next_date')[:count]
        for learning_word in learning_words:
            result.append(dict(
                id=learning_word.id,
                word_text=learning_word.word.word_text,
                meaning=TranslatedWord.objects.get(
                    language=user.userinfo.language,
                    word=learning_word.word,
                ).meaning,
                state=learning_word.state,
            ))
        return result


class ClearedPackage(models.Model):
    package = models.ForeignKey(Package)
    user = models.ForeignKey(User)
    cleared_date = models.DateTimeField(default=timezone.now)
