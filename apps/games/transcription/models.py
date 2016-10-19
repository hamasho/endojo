from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Package(models.Model):
    title = models.CharField(max_length=200, unique=True)
    level = models.SmallIntegerField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-pub_date']


class Problem(models.Model):
    question_text = models.CharField(max_length=200)
    package = models.ForeignKey(Package)


class ProblemScore(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    response_time_ms = models.IntegerField()
    update_date = models.DateTimeField(default=timezone.now)

    def save_score(user, problem_id, response_time_ms):
        problem = Problem.objects.get(id=problem_id)
        problem_score = ProblemScore.get_or_create(
            user=user,
            problem=problem,
            defaults={'response_time_ms': response_time_ms}
        )
        problem_score.save()
