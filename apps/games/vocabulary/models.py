from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from registration.models import Language
from core.utils import date_range, get_today


class Package(models.Model):
    title = models.CharField(max_length=200, unique=True)
    level = models.SmallIntegerField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-pub_date']

    @staticmethod
    def get_package_list(user, language):
        packages = Package.objects.filter(
            availablepackage__language=language,
        ).order_by('level', 'title')
        result = []
        for package in packages:
            try:
                state = PackageState.objects.get(
                    user=user,
                    package=package,
                )
                state = 'Complete' if state.complete else 'Learning'
            except PackageState.DoesNotExist:
                state = 'Yet'
            n_tried = PackageState.objects.filter(
                package=package,
            ).count()
            n_completed = PackageState.objects.filter(
                package=package,
                complete=True,
            ).count()

            result.append({
                'id': package.id,
                'title': package.title,
                'level': package.level,
                'pub_date': package.pub_date,
                'state': state,
                'n_tried': n_tried,
                'n_completed': n_completed,
            })

        return result


class AvailablePackage(models.Model):
    package = models.ForeignKey(Package)
    language = models.ForeignKey(Language)

    class Meta:
        unique_together = ('package', 'language')


class PackageState(models.Model):
    user = models.ForeignKey(User)
    package = models.ForeignKey(Package)
    complete = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'package')


class Word(models.Model):
    word_text = models.CharField(max_length=40, unique=True)
    package = models.ForeignKey(Package)

    @staticmethod
    def get_translated_words(package_id, language):
        """
        Return translated word objects
        [{
            "id": word.id,
            "word_text": word.word_text,
            "meaning": meaning
        }, ...]
        """
        t_words = TranslatedWord.objects.filter(
            word__package_id=package_id,
            language=language,
        ).prefetch_related('word')
        result = []
        for t_word in t_words:
            result.append({
                'id': t_word.word.id,
                'word_text': t_word.word.word_text,
                'meaning': t_word.meaning,
            })
        return result


class TranslatedWord(models.Model):
    word = models.ForeignKey(Word)
    language = models.ForeignKey(Language)
    meaning = models.CharField(max_length=100)

    class Meta:
        unique_together = ('word', 'language')


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
    added = models.DateField(auto_now_add=True)
    next_date = models.DateField(default=get_today)

    class Meta:
        unique_together = ('user', 'word')

    def level_up(self):
        """
        Count up the state of WordState.
        If the state become 6, then check other words in the same package
        and if there is no words with level less than 6,
        change the user's package state to `complete = True`.
        Finally, save the current word state.
        """
        self.state += 1
        if (self.state == 6):
            self.save()
            n_remaining_words = WordState.objects.filter(
                word__package=self.word.package,
                user=self.user,
            ).exclude(
                state=6,
            ).count()
            # If all words in the package complete learning,
            # update the package state as `complete = True.`
            if n_remaining_words == 0:
                package_state = PackageState.objects.get(
                    user=self.user,
                    package=self.word.package,
                )
                package_state.complete = True
                package_state.save()
            return

        if (self.state == 2):
            delta = timedelta(days=1)
        elif (self.state == 3):
            delta = timedelta(days=3)
        elif (self.state == 4):
            delta = timedelta(days=7)
        elif (self.state == 5):
            delta = timedelta(days=14)
        self.next_date = get_today() + delta
        self.save()

    def level_reset(self):
        self.state = 1
        self.next_date = get_today()
        self.save()

    @staticmethod
    def get_learning_words(user, count):
        result = []
        learning_words = WordState.objects.filter(
            user=user,
            state__lte=5,
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


class History(models.Model):
    user = models.ForeignKey(User, related_name='vocabulary_history_user')
    n_failed = models.SmallIntegerField(default=0)
    n_complete = models.SmallIntegerField(default=0)
    n_levelup = models.SmallIntegerField(default=0)
    n_state1 = models.IntegerField(default=0)
    n_state2 = models.IntegerField(default=0)
    n_state3 = models.IntegerField(default=0)
    n_state4 = models.IntegerField(default=0)
    n_state5 = models.IntegerField(default=0)
    n_state6 = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    @staticmethod
    def get_formatted_stats(user):
        result = {
            'state1': [],
            'state2': [],
            'state3': [],
            'state4': [],
            'state5': [],
            'state6': [],
        }
        histories = History.objects.filter(user=user)
        if len(histories) == 0:
            return result
        start_date = histories[0].date
        end_date = histories[len(histories) - 1].date
        for date in date_range(start_date, end_date + timedelta(1)):
            that_day = histories.filter(date=date)
            if not that_day.exists():
                continue
            that_day = that_day[0]
            result['state1'].append({
                'x': date,
                'y': that_day.n_state1,
            })
            result['state2'].append({
                'x': date,
                'y': that_day.n_state2,
            })
            result['state3'].append({
                'x': date,
                'y': that_day.n_state3,
            })
            result['state4'].append({
                'x': date,
                'y': that_day.n_state4,
            })
            result['state5'].append({
                'x': date,
                'y': that_day.n_state5,
            })
            result['state6'].append({
                'x': date,
                'y': that_day.n_state6,
            })
        return result
