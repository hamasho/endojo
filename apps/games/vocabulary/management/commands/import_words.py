# Import each translation files.
# Translation files are located in game_data/vocabulary
# as following structure.
#
#  +- words
#  |   +- 1_Basic_Words_1
#  |   +- 1_Basic_Words_2
#  |   +- [LEVEL]_[TITLE]
#  |
#  +- translations
#      +- Japanese
#      |   +- 1_Basic_Words_1
#      |   +- 1_Basic_Words_2
#      |   +- [LEVEL]_[TITLE]
#      |
#      +- Spanish
#      |   +- 1_Basic_Words_1
#      |
#      +- ...
#
# LEVEL: The level of package.
# TITLE: The title of package. Spaces are converted to underscores.
#
# And each translation file contains corresponding translations.
#
# -- words/1_Basic_Words_1 --
# more
# some
# ...
# ---------------------------
#
# -- translation/Japanese/1_Basic_Words_1 --
# [translated word `more` in Japanese]
# [translated word `some` in Japanese]
# ...
# ------------------------------------------
import os
from django.core.management.base import BaseCommand
from django.db import transaction

from endojo import settings
from registration.models import Language
from vocabulary.models import Package, Word, TranslatedWord

BASE_DIR = os.path.join(settings.BASE_DIR, 'game_data/vocabulary')
WORD_DIR = os.path.join(BASE_DIR, 'words')
TRANSLATION_DIR = os.path.join(BASE_DIR, 'translations')


def get_lines(file_path):
    with open(file_path) as file:
        return [line.rstrip('\n') for line in file]


def import_english_words(word_file_name):
    word_file_path = os.path.join(WORD_DIR, word_file_name)
    words = get_lines(word_file_path)
    title = word_file_name[2:].replace('_', ' ')
    level = word_file_name[0]
    if (Package.objects.filter(title=title).count() > 0):
        return
    package = Package.objects.create(
        title=title,
        level=level,
    )
    for word in words:
        Word.objects.create(
            word_text=word,
            package=package,
        )
    print('Add package: %s' % title)


def import_each_translation(word_file_name):
    languages = Language.objects.all()
    translation_dirs = os.listdir(TRANSLATION_DIR)
    for language in languages:
        lang = language.language_text
        if lang not in translation_dirs:
            continue

        translation_file_path = os.path.join(TRANSLATION_DIR, lang)
        for file_name in os.listdir(translation_file_path):
            package_title = file_name[2:].replace('_', ' ')
            package = Package.objects.get(title=package_title)
            current_translations = TranslatedWord.objects.filter(
                word__package=package,
                language=language,
            )
            if current_translations.count() > 0:
                continue
            words = get_lines(os.path.join(WORD_DIR, file_name))
            translations = get_lines(os.path.join(translation_file_path, file_name))
            for i in range(len(words)):
                TranslatedWord.objects.create(
                    word=Word.objects.get(word_text=words[i]),
                    language=language,
                    meaning=translations[i],
                )
            print('Add translation %s (%s)' % (package_title, lang))


class Command(BaseCommand):
    help = 'Import vocabulary game\'s word files'

    def handle(self, *args, **options):
        files = os.listdir(WORD_DIR)

        for word_file_name in files:
            with transaction.atomic():
                import_english_words(word_file_name)
                import_each_translation(word_file_name)
