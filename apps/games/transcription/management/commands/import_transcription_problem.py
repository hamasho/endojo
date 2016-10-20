import os
from django.core.management.base import BaseCommand
from django.db import transaction

from endojo import settings
from transcription.models import Package, Problem


class Command(BaseCommand):
    help = 'Add transcription game problems from files'

    def handle(self, *args, **options):
        base_dir = os.path.join(settings.BASE_DIR, 'game_data/transcription')
        files = os.listdir(base_dir)

        with transaction.atomic():
            for filename in files:
                filepath = os.path.join(base_dir, filename)
                lines = [line.rstrip('\n') for line in open(filepath)]
                title = lines[0]
                level = lines[1]
                if Package.objects.filter(title=title).count() > 0:
                    continue
                package = Package(
                    title=title,
                    level=level
                )
                package.save()
                for line in lines[2:]:
                    Problem.objects.create(
                        problem_text=line,
                        package=package
                    )
                self.stdout.write('Add package: %s' % (title,))
