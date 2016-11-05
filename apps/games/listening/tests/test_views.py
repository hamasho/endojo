import json
from django.test import TestCase
from django.urls import reverse

from listening import models


class ResultStoreApiTest(TestCase):
    fixtures = ['auth.User.json', 'listening/Package.json', 'listening/Problem.json']

    def setUp(self):
        self.client.login(username='user1', password='password')

    def test_storing_game_score(self):
        expected = {
            'status': 'ok',
        }
        response = self.client.post(
            reverse('listening:result_store_api'),
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
