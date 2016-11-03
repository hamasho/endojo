import datetime
import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from transcription import models


def create_time(y, m, d):
    return timezone.make_aware(
        datetime.datetime(y, m, d),
        timezone.get_current_timezone()
    )


class PackageListApiTest(TestCase):
    fixtures = ['auth.User.json']

    def setUp(self):
        self.client.login(username='shinsuke', password='password')

    def test_with_zero_package(self):
        response = self.client.get(reverse('transcription:package_api'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'packages': []})

    def test_with_one_package(self):
        """
        PackageListApi view must return one package in JSON response
        """
        models.Package.objects.create(
            title="Test",
            level=1,
            pub_date=create_time(2016, 10, 22)
        )
        expected = {
            'packages': [{
                'id': 1,
                'title': 'Test',
                'level': 1,
                'pub_date': '2016-10-22T00:00:00Z',
                'n_tried': 0,
                'n_completed': 0,
            }],
        }
        response = self.client.get(reverse('transcription:package_api'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected)

    def test_with_two_package(self):
        """
        PackageListApi view must return one package in JSON response
        """
        models.Package.objects.create(
            title="Test",
            level=1,
            pub_date=create_time(2016, 10, 22)
        )
        models.Package.objects.create(
            title="Test 2",
            level=2,
            pub_date=create_time(2016, 10, 30)
        )
        expected = {
            'packages': [{
                'id': 2,
                'title': 'Test 2',
                'level': 2,
                'pub_date': '2016-10-30T00:00:00Z',
                'n_tried': 0,
                'n_completed': 0,
            }, {
                'id': 1,
                'title': 'Test',
                'level': 1,
                'pub_date': '2016-10-22T00:00:00Z',
                'n_tried': 0,
                'n_completed': 0,
            }],
        }
        response = self.client.get(reverse('transcription:package_api'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected)


class ProblemListApiTest(TestCase):
    fixtures = ['auth.User.json', 'transcription.Package.json', 'transcription.Problem.json']

    def setUp(self):
        self.client.login(username='shinsuke', password='password')

    def test_with_two_problems_on_one_package(self):
        response = self.client.get(reverse('transcription:problem_api', args=[1]))
        expected = {
            'result': [{
                'id': 1,
                'problem_text': 'This is a pen.',
                'package_id': 1,
                'level': 1,
            }, {
                'id': 2,
                'problem_text': 'Cats are cute.',
                'package_id': 1,
                'level': 1,
            }, {
                'id': 3,
                'problem_text': 'Cats are cute.',
                'package_id': 1,
                'level': 2,
            }, {
                'id': 4,
                'problem_text': 'Cats are cute.',
                'package_id': 1,
                'level': 2,
            }],
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected)


class ResultStoreApiTest(TestCase):
    fixtures = ['auth.User.json', 'transcription.Package.json', 'transcription.Problem.json']

    def setUp(self):
        self.client.login(username='shinsuke', password='password')

    def test_storing_game_score(self):
        expected = {
            'status': 'ok',
        }
        response = self.client.post(
            reverse('transcription:result_store_api'),
            json.dumps({
                'package': {
                    'id': 1,
                },
                'score': [
                    {
                        'id': 1,
                        'responseTimeMs': 3000,
                        'complete': True,
                    }, {
                        'id': 2,
                        'complete': False,
                    }, {
                        'id': 3,
                        'responseTimeMs': 4000,
                        'complete': True,
                    }, {
                        'id': 4,
                        'responseTimeMs': 3000,
                        'complete': True,
                    },
                ],
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected)
        p1 = models.ProblemScore.objects.get(pk=1)
        p2 = models.ProblemScore.objects.get(pk=2)
        p3 = models.ProblemScore.objects.get(pk=3)
        self.assertEqual(p1.response_time_ms, 3000)
        self.assertTrue(p1.complete)
        self.assertEqual(p2.response_time_ms, None)
        self.assertFalse(p2.complete)
        self.assertEqual(p3.response_time_ms, 4000)
        self.assertTrue(p3.complete)
        ps = models.PackageState.objects.get(pk=1)
        self.assertFalse(ps.complete)
        h = models.History.objects.get(pk=2)
        self.assertEqual(h.user.id, 1)
        self.assertEqual(h.level, 2)
        self.assertEqual(h.problem_count, 2)
        self.assertEqual(h.average_time_ms, 3500)


class StatsApiTest(TestCase):
    fixtures = ['auth.User.json', 'transcription.Package.json', 'transcription.Problem.json']

    def setUp(self):
        self.client.login(username='shinsuke', password='password')

    def test_get_stats(self):
        response = self.client.get(reverse('transcription:stats_api'))
        self.assertEqual(response.status_code, 200)
