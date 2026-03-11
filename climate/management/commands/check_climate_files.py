from django.core.management.base import BaseCommand
from climate.models import ClimateFile

class Command(BaseCommand):
    help = 'List all climate files in the database'

    def handle(self, *args, **kwargs):
        files = ClimateFile.objects.all()
        if not files:
            self.stdout.write(self.style.WARNING('No files found in database'))
        else:
            for f in files:
                self.stdout.write(f"Variable: {f.variable_name}")
                self.stdout.write(f"Path: {f.file_path}")
                self.stdout.write(f"Name: {f.file_name}")
                self.stdout.write("---")
