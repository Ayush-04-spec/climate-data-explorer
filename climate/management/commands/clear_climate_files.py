from django.core.management.base import BaseCommand
from climate.models import ClimateFile

class Command(BaseCommand):
    help = 'Clear all climate files from the database'

    def handle(self, *args, **kwargs):
        count = ClimateFile.objects.all().count()
        ClimateFile.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} climate file entries')
        )
