from django.test import TestCase
from django.urls import reverse


class HistoryApiTest(TestCase):
    fixtures = [
        'auth.User.json',
        'vocabulary/History.json',
        'listening/History.json',
        'transcription/History.json',
    ]

    def setUp(self):
        self.client.login(username='user1', password='password')

    def test_storing_game_score(self):
        response = self.client.get(reverse('mypage:history_api'))
        self.assertEqual(response.status_code, 200)
