import os
import glob
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.db import transaction

from endojo import settings
from listening.models import Package, Problem


class Command(BaseCommand):
    help = 'Import listening game\'s problem files'

    def handle(self, *args, **options):
        base_dir = os.path.join(settings.BASE_DIR, 'game_data/listening')
        dirs = os.listdir(base_dir)

        for dirname in dirs:
            with transaction.atomic():
                dirpath = os.path.join(base_dir, dirname)
                info_filepath = os.path.join(dirpath, 'info.txt')
                lines = [line.rstrip('\n') for line in open(info_filepath)]
                title = lines[0]
                problems = lines[1:]
                if Package.objects.filter(title=title).count() > 0:
                    continue

                audio_files = sorted(glob.glob('%s/*.mp3' % (dirpath)))
                if len(problems) != len(audio_files):
                    raise CommandError("Info file does not match actual audio files")

                package = Package.objects.create(
                    title=title,
                    level=1,
                )
                level_sum = 0

                for i in range(len(problems)):
                    line = problems[i]
                    length = len(line)
                    if length <= 30:
                        level = 1
                    elif length <= 45:
                        level = 2
                    elif length <= 60:
                        level = 3
                    elif length <= 75:
                        level = 4
                    else:
                        level = 5
                    problem = Problem.objects.create(
                        problem_text=line,
                        package=package,
                        level=level,
                    )
                    audio_filepath = audio_files[i]
                    audio_file = File(open(audio_filepath, mode='rb'))
                    problem.audio_file = audio_file
                    problem.save()
                    level_sum += level

                package.level = int(round((level_sum + 0.0) / len(lines[1:])))
                package.save()
                self.stdout.write('Add package: %s' % (title,))
