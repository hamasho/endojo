import json
from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth.models import User

from vocabulary import models


class ResultStoreApiTest(TestCase):
    fixtures = [
        'auth.User.json',
        'vocabulary/Package.json',
        'vocabulary/Word.json',
        'vocabulary/WordState.json',
    ]

    def setUp(self):
        self.client.login(username='user1', password='password')

    def test_post(self):
        expected = {'status': 'ok'}
        response = self.client.post(
            reverse('vocabulary:result_store_api'),
            json.dumps({
                'failed': [
                    {'id': 2},
                ],
                'answered': [
                    {'id': 1},
                    {'id': 3},
                ],
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected)
        s1 = models.WordState.objects.get(pk=1)
        s2 = models.WordState.objects.get(pk=2)
        s3 = models.WordState.objects.get(pk=3)
        self.assertEqual(s1.state, 2)
        self.assertEqual(s2.state, 1)
        self.assertEqual(s3.state, 6)
        history = models.History.objects.get(pk=1)
        self.assertEqual(history.n_failed, 1)
        self.assertEqual(history.n_complete, 1)
        self.assertEqual(history.n_levelup, 1)
