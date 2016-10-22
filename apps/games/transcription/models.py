import datetime
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from core.utils import date_range


class Package(models.Model):
    title = models.CharField(max_length=200, unique=True)
    level = models.SmallIntegerField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-pub_date']


class Problem(models.Model):
    problem_text = models.CharField(max_length=200)
    package = models.ForeignKey(Package)
    level = models.SmallIntegerField()


class ProblemScore(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    response_time_ms = models.IntegerField()
    update_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        When saving scores, also have to update History model.
        """
        today, created = History.objects.get_or_create(
            user=self.user,
            level=self.problem.level,
            date=datetime.date.today()
        )
        avg = today.problem_count * today.average_time_ms
        today.problem_count += 1
        today.average_time_ms = \
            (avg + self.response_time_ms) / today.problem_count
        today.save()
        super(ProblemScore, self).save(*args, **kwargs)


class History(models.Model):
    user = models.ForeignKey(User)
    level = models.SmallIntegerField()
    problem_count = models.IntegerField(default=0)
    average_time_ms = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    @staticmethod
    def get_formatted_stats(user):
        """
        Format user's score data to fit Chart.js data structure
        """
        result = {
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
        }
        histories = History.objects.filter(user=user)
        if len(histories) == 0:
            return result
        start_date = histories[0].date
        end_date = histories[len(histories) - 1].date
        index = 0
        for date in date_range(start_date, end_date + timedelta(1)):
            histories_at = histories.filter(date=date)
            for history in histories_at:
                result[str(history.level)] += [{
                    'x': index,
                    'y': history.average_time_ms,
                }]
            index += 1
        return result

    class Meta:
        ordering = ['date']
