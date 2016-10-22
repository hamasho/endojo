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


class ViewsTest(TestCase):
    fixtures = ['auth.User.json']

    def test_anonymouse_user_cannot_get_pages(self):
        """
        Users must not be able to get these pages without logging in
        """
        urls = [
            'transcription:game',
            'transcription:package_api',
            'transcription:stats_api',
        ]
        for url in urls:
            response = self.client.get(reverse(url))
            expected = "%s?next=%s" % (reverse('registration:login'), reverse(url))
            self.assertRedirects(response, expected)

    def test_logged_in_user_can_get_pages(self):
        """
        Logged in users can get these pages
        """
        urls = [
            'transcription:game',
            'transcription:package_api',
            'transcription:stats_api',
        ]
        self.client.login(username='shinsuke', password='password')
        for url in urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)


class PackageListApiTest(TestCase):
    fixtures = ['auth.User.json']

    def setUp(self):
        self.client.login(username='shinsuke', password='password')

    def test_with_zero_package(self):
        response = self.client.get(reverse('transcription:package_api'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'result': []})

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
            'result': [{
                'id': 1,
                'title': 'Test',
                'level': 1,
                'pub_date': '2016-10-22T00:00:00Z',
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
            'result': [{
                'id': 2,
                'title': 'Test 2',
                'level': 2,
                'pub_date': '2016-10-30T00:00:00Z',
            }, {
                'id': 1,
                'title': 'Test',
                'level': 1,
                'pub_date': '2016-10-22T00:00:00Z',
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
                'score': [
                    {
                        'id': 1,
                        'responseTimeMs': 3000,
                    }, {
                        'id': 2,
                        'responseTimeMs': 5000,
                    },
                ],
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected)
        p1 = models.ProblemScore.objects.get(pk=1)
        p2 = models.ProblemScore.objects.get(pk=2)
        self.assertEqual(p1.response_time_ms, 3000)
        self.assertEqual(p2.response_time_ms, 5000)
        h = models.History.objects.get(pk=1)
        self.assertEqual(h.user.id, 1)
        self.assertEqual(h.level, 1)
        self.assertEqual(h.problem_count, 2)
        self.assertEqual(h.average_time_ms, 4000)


class StatsApiTest(TestCase):
    fixtures = ['auth.User.json', 'transcription.Package.json', 'transcription.Problem.json']

    def setUp(self):
        self.client.login(username='shinsuke', password='password')

    def test_get_stats(self):
        response = self.client.get(reverse('transcription:stats_api'))
        self.assertEqual(response.status_code, 200)
