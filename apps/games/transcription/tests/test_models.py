from django.test import TestCase
from django.contrib.auth.models import User

from transcription import models


class ProblemScoreTest(TestCase):
    fixtures = ['auth.User.json', 'transcription.Package.json', 'transcription.Problem.json']

    def test_save_works_correctly(self):
        user = User.objects.get(pk=1)
        problem = models.Problem.objects.get(pk=1)
        score = models.ProblemScore(
            user=user,
            problem=problem,
            response_time_ms=3000
        )
        score.save()
        history = models.History.objects.get(pk=1)
        self.assertEqual(history.user_id, 1)
        self.assertEqual(history.level, 1)
        self.assertEqual(history.problem_count, 1)
        self.assertEqual(history.average_time_ms, 3000)
        self.assertEqual(models.History.objects.count(), 1)

        problem = models.Problem.objects.get(pk=2)
        score = models.ProblemScore(
            user=user,
            problem=problem,
            response_time_ms=5000
        )
        score.save()
        history = models.History.objects.get(pk=1)
        self.assertEqual(history.user_id, 1)
        self.assertEqual(history.level, 1)
        self.assertEqual(history.problem_count, 2)
        self.assertEqual(history.average_time_ms, 4000)
        self.assertEqual(models.History.objects.count(), 1)

        problem = models.Problem.objects.get(pk=3)
        score = models.ProblemScore(
            user=user,
            problem=problem,
            response_time_ms=3000
        )
        score.save()
        history = models.History.objects.get(pk=2)
        self.assertEqual(history.user_id, 1)
        self.assertEqual(history.level, 2)
        self.assertEqual(history.problem_count, 1)
        self.assertEqual(history.average_time_ms, 3000)
        self.assertEqual(models.History.objects.count(), 2)


class HistoryTest(TestCase):
    fixtures = ['auth.User.json', 'transcription.History.json']

    def test_with_normal_data(self):
        user = User.objects.get(pk=1)
        stats = models.History.get_formatted_stats(user)
        self.assertEqual(stats['1'], [
            {'x': 1, 'y': 4000},
            {'x': 2, 'y': 3000},
            {'x': 4, 'y': 4000},
            {'x': 6, 'y': 2000},
        ])
        self.assertEqual(stats['2'], [
            {'x': 0, 'y': 4000},
            {'x': 3, 'y': 3000},
            {'x': 7, 'y': 2000},
        ])
        self.assertEqual(stats['3'], [])
        self.assertEqual(stats['4'], [])
        self.assertEqual(stats['5'], [])
