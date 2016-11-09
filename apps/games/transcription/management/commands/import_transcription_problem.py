import os
from django.core.management.base import BaseCommand
from django.db import transaction

from endojo import settings
from transcription.models import Package, Problem


class Command(BaseCommand):
    help = 'Import transcription game\'s problems files'

    def handle(self, *args, **options):
        base_dir = os.path.join(settings.base.BASE_DIR, 'game_data/transcription')
        files = os.listdir(base_dir)

        with transaction.atomic():
            for filename in files:
                filepath = os.path.join(base_dir, filename)
                lines = [line.rstrip('\n') for line in open(filepath)]
                title = lines[0]
                level_sum = 0
                if Package.objects.filter(title=title).count() > 0:
                    continue
                package = Package.objects.create(
                    title=title,
                    level=1,
                )
                for line in lines[1:]:
                    length = len(line)
                    if length <= 25:
                        level = 1
                    elif length <= 37:
                        level = 2
                    elif length <= 50:
                        level = 3
                    elif length <= 63:
                        level = 4
                    else:
                        level = 5
                    Problem.objects.create(
                        problem_text=line,
                        package=package,
                        level=level
                    )
                    level_sum += level
                package.level = int(round((level_sum + 0.0) / len(lines[1:])))
                package.save()
                self.stdout.write('Add package: %s' % (title,))
