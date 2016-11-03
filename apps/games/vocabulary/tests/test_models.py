from datetime import timedelta
from django.test import TestCase
from django.contrib.auth.models import User

from core.utils import today
from vocabulary import models
from registration.models import Language


class WordTest(TestCase):
    fixtures = [
        'registration/Language.json',
        'vocabulary/Package.json',
        'vocabulary/Word.json',
        'vocabulary/TranslatedWord.json',
    ]

    def test_get_translated_words(self):
        lang = Language.objects.get(pk=1)
        result = models.Word.get_translated_words(1, lang)
        self.assertEqual(result, [{
            'id': 1,
            'word_text': 'more',
            'meaning': u'より多くの',
        }, {
            'id': 2,
            'word_text': 'some',
            'meaning': u'いくつかの',
        }, {
            'id': 3,
            'word_text': 'all',
            'meaning': u'すべて',
        }])


class WordStateTest(TestCase):
    fixtures = [
        'auth.User.json',
        'registration/Language.json',
        'registration/UserInfo.json',
        'vocabulary/Package.json',
        'vocabulary/Word.json',
        'vocabulary/TranslatedWord.json',
    ]

    def test_level_up(self):
        state = models.WordState(
            user=User.objects.get(pk=1),
            word=models.Word.objects.get(pk=1),
        )
        self.assertEqual(state.state, 1)
        self.assertEqual(state.next_date, today())

        state.level_up()
        self.assertEqual(state.next_date, today() + timedelta(days=1))
        self.assertEqual(state.state, 2)
        state.level_up()
        self.assertEqual(state.next_date, today() + timedelta(days=3))
        self.assertEqual(state.state, 3)
        state.level_up()
        self.assertEqual(state.next_date, today() + timedelta(days=7))
        self.assertEqual(state.state, 4)
        state.level_up()
        self.assertEqual(state.next_date, today() + timedelta(days=14))
        self.assertEqual(state.state, 5)

    def test_level_up_update_package_state(self):
        state1 = models.WordState.objects.create(
            user=User.objects.get(pk=1),
            word=models.Word.objects.get(pk=1),
            state=5,
        )
        state2 = models.WordState.objects.create(
            user=User.objects.get(pk=1),
            word=models.Word.objects.get(pk=2),
            state=5,
        )
        ps = models.PackageState.objects.create(
            user=User.objects.get(pk=1),
            package=models.Package.objects.get(pk=1),
            complete=False,
        )

        state1.level_up()
        ps = models.PackageState.objects.get(pk=1)
        self.assertFalse(ps.complete)
        state2.level_up()
        ps = models.PackageState.objects.get(pk=1)
        self.assertTrue(ps.complete)

    def test_level_reset(self):
        state = models.WordState.objects.create(
            user=User.objects.get(pk=1),
            word=models.Word.objects.get(pk=1),
            state=3,
        )
        state.level_reset()
        self.assertEqual(state.state, 1)
        self.assertEqual(state.next_date, today())

    def test_get_learning_words(self):
        state1 = models.WordState.objects.create(
            user=User.objects.get(pk=1),
            word=models.Word.objects.get(pk=1),
            state=5,
        )
        state2 = models.WordState.objects.create(
            user=User.objects.get(pk=1),
            word=models.Word.objects.get(pk=2),
            state=4,
        )
        state3 = models.WordState.objects.create(
            user=User.objects.get(pk=1),
            word=models.Word.objects.get(pk=3),
            state=3,
        )

        result = models.WordState.get_learning_words(
            user=User.objects.get(pk=1),
            count=2,
        )
        self.assertEqual(result, [{
            'id': 1,
            'word_text': 'more',
            'meaning': u'より多くの',
            'state': 5,
        }, {
            'id': 2,
            'word_text': 'some',
            'meaning': u'いくつかの',
            'state': 4,
        }])

        state2.level_up()
        result = models.WordState.get_learning_words(
            user=User.objects.get(pk=1),
            count=2,
        )
        self.assertEqual(result, [{
            'id': 1,
            'word_text': 'more',
            'meaning': u'より多くの',
            'state': 5,
        }, {
            'id': 3,
            'word_text': 'all',
            'meaning': u'すべて',
            'state': 3,
        }])

        state1.level_up()
        state2.level_reset()
        state3.level_up()
        result = models.WordState.get_learning_words(
            user=User.objects.get(pk=1),
            count=2,
        )
        self.assertEqual(result, [{
            'id': 2,
            'word_text': 'some',
            'meaning': u'いくつかの',
            'state': 1,
        }])
