import datetime
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from listening import models


def create_time(y, m, d):
    return timezone.make_aware(
        datetime.datetime(y, m, d),
        timezone.get_current_timezone()
    )


class PackageTest(TestCase):
    fixtures = ['auth.User.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_with_packages(self):
        # With one package
        models.Package.objects.create(
            title="Test",
            level=1,
            pub_date=create_time(2016, 10, 22)
        )
        expected = [{
            'id': 1,
            'title': 'Test',
            'level': 1,
            'pub_date': create_time(2016, 10, 22),
            'state': 'Yet',
            'n_tried': 0,
            'n_completed': 0,
        }]
        actual = models.Package.get_package_list(self.user)
        self.assertEqual(actual, expected)

        # 1 package with 1 uncomplete user
        models.PackageState.objects.create(
            user=User.objects.get(pk=2),
            package=models.Package.objects.get(pk=1),
            complete=False,
        )
        expected = [{
            'id': 1,
            'title': 'Test',
            'level': 1,
            'pub_date': create_time(2016, 10, 22),
            'state': 'Yet',
            'n_tried': 1,
            'n_completed': 0,
        }]
        actual = models.Package.get_package_list(self.user)
        self.assertEqual(actual, expected)

        # 1 package with 1 complete user
        models.PackageState.objects.filter(user_id=2).update(
            complete=True,
        )
        expected = [{
            'id': 1,
            'title': 'Test',
            'level': 1,
            'pub_date': create_time(2016, 10, 22),
            'state': 'Yet',
            'n_tried': 1,
            'n_completed': 1,
        }]
        actual = models.Package.get_package_list(self.user)
        self.assertEqual(actual, expected)

        # user uncomplete the package
        models.PackageState.objects.create(
            user=self.user,
            package=models.Package.objects.get(pk=1),
            complete=False,
        )
        expected = [{
            'id': 1,
            'title': 'Test',
            'level': 1,
            'pub_date': create_time(2016, 10, 22),
            'state': 'Learning',
            'n_tried': 2,
            'n_completed': 1,
        }]
        actual = models.Package.get_package_list(self.user)
        self.assertEqual(actual, expected)

        # user complete the package
        models.PackageState.objects.filter(user_id=1).update(
            complete=True,
        )
        expected = [{
            'id': 1,
            'title': 'Test',
            'level': 1,
            'pub_date': create_time(2016, 10, 22),
            'state': 'Complete',
            'n_tried': 2,
            'n_completed': 2,
        }]
        actual = models.Package.get_package_list(self.user)
        self.assertEqual(actual, expected)

        # 2 package with 1 uncomplete and 1 complete
        models.Package.objects.create(
            title='Test 2',
            level=1,
            pub_date=create_time(2016, 10, 22),
        )
        models.PackageState.objects.create(
            user=User.objects.get(pk=2),
            package=models.Package.objects.get(pk=2),
            complete=False,
        )
        expected = [{
            'id': 1,
            'title': 'Test',
            'level': 1,
            'pub_date': create_time(2016, 10, 22),
            'state': 'Complete',
            'n_tried': 2,
            'n_completed': 2,
        }, {
            'id': 2,
            'title': 'Test 2',
            'level': 1,
            'pub_date': create_time(2016, 10, 22),
            'state': 'Yet',
            'n_tried': 1,
            'n_completed': 0,
        }]
        actual = models.Package.get_package_list(self.user)
        self.assertEqual(actual, expected)


class ProblemScoreTest(TestCase):
    fixtures = [
        'auth.User.json',
        'listening/Package.json',
        'listening/Problem.json'
    ]

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
    fixtures = ['auth.User.json', 'listening/History.json']

    def test_with_normal_data(self):
        user = User.objects.get(pk=1)
        stats = models.History.get_formatted_stats(user)
        self.assertEqual(stats['1'], [
            {'x': datetime.date(2016, 10, 21), 'y': 4.0},
            {'x': datetime.date(2016, 10, 22), 'y': 3.0},
            {'x': datetime.date(2016, 10, 24), 'y': 4.0},
            {'x': datetime.date(2016, 10, 26), 'y': 2.0},
        ])
        self.assertEqual(stats['2'], [
            {'x': datetime.date(2016, 10, 20), 'y': 4.0},
            {'x': datetime.date(2016, 10, 23), 'y': 3.0},
            {'x': datetime.date(2016, 10, 27), 'y': 2.0},
        ])
        self.assertEqual(stats['3'], [])
        self.assertEqual(stats['4'], [])
        self.assertEqual(stats['5'], [])
