from django.db import models
from django.utils import timezone


class Package(models.Model):
    title = models.CharField(max_length=200, unique=True)
    level = models.SmallIntegerField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-pub_date']


class Problem(models.Model):
    question_text = models.CharField(max_length=200)
    package = models.ForeignKey(Package)
