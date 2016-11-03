import os
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

    @staticmethod
    def get_package_list(user):
        packages = Package.objects.all()
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


def upload_directory(instance, filename):
    basename = os.path.basename(filename)
    return 'listening_audio/%d/%s' % (instance.package.id, basename)


class Problem(models.Model):
    problem_text = models.CharField(max_length=200)
    package = models.ForeignKey(Package)
    audio_file = models.FileField(upload_to=upload_directory)
    level = models.SmallIntegerField()


class PackageState(models.Model):
    """
    A state which shows an user has completed the package or not.
    If `complete` is `True`, he/she has completed.
    If `false`, he/she tried but gave up.
    """
    user = models.ForeignKey(User, related_name='listening_packagestate_user')
    package = models.ForeignKey(Package)
    complete = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'package')


class ProblemScore(models.Model):
    user = models.ForeignKey(User, related_name='listening_problemscore_user')
    problem = models.ForeignKey(Problem)
    response_time_ms = models.IntegerField(null=True)
    complete = models.BooleanField(default=True)
    update_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'problem')

    def save(self, *args, **kwargs):
        """
        When saving scores, also have to update History model.
        """
        if self.complete:
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
    user = models.ForeignKey(User, related_name='listening_history_user')
    level = models.SmallIntegerField()
    problem_count = models.IntegerField(default=0)
    average_time_ms = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']

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
        for date in date_range(start_date, end_date + timedelta(1)):
            histories_at = histories.filter(date=date)
            for history in histories_at:
                result[str(history.level)] += [{
                    'x': date,
                    'y': history.average_time_ms / 1000,
                }]
        return result
