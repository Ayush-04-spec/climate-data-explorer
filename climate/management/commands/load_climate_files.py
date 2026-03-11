from django.core.management.base import BaseCommand
from climate.models import ClimateFile

class Command(BaseCommand):
    help = 'Load climate file paths into the database'

    def handle(self, *args, **kwargs):

        # Remove old entries to avoid duplicates or wrong paths
        ClimateFile.objects.all().delete()

        climate_files = [
            {
                'variable_name': 'tas',
                'file_path': 'C:/climate_data/2m_temperature_0_daily-mean.nc',
                'file_name': '2m_temperature_0_daily-mean.nc'
            },
            {
                'variable_name': 'pr',
                'file_path': 'C:/climate_data/total_precipitation_0_daily-mean.nc',
                'file_name': 'total_precipitation_0_daily-mean.nc'
            },
            {
                'variable_name': 'vas',
                'file_path': 'C:/climate_data/10m_v_component_of_wind_0_daily-mean.nc',
                'file_name': '10m_v_component_of_wind_0_daily-mean.nc'
            }
        ]

        for file_data in climate_files:
            ClimateFile.objects.create(
                variable_name=file_data['variable_name'],
                file_path=file_data['file_path'],
                file_name=file_data['file_name']
            )

            self.stdout.write(self.style.SUCCESS(f"Loaded {file_data['file_name']}"))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all climate files'))