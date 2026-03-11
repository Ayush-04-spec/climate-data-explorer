from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import xarray as xr
import pandas as pd
import io
from datetime import datetime
import psycopg2
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Database configuration
DB_CONFIG = settings.DB_CONFIG

# ERA5 variable mapping
VARIABLE_MAP = {
    "tas": "t2m",
    "pr": "tp",
    "vas": "v10"
}


def get_file_paths(variable_name):
    """Retrieve file paths for the given climate variable."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT file_path FROM climate_files WHERE variable_name = %s",
        (variable_name,)
    )
    paths = [row[0] for row in cursor.fetchall()]
    conn.close()
    return paths


climate_variables = ['vas', 'tas', 'pr']


def home(request):
    return render(request, 'index.html', {'climate_variables': climate_variables})


@login_required
def get_timeseries(request):
    try:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        variable_name = request.GET.get('variable')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        coordinates = request.GET.get('coordinates')

        if not variable_name or not start_date or not end_date:
            return JsonResponse(
                {'error': 'Variable, start date, and end date are required.'},
                status=400
            )

        file_paths = get_file_paths(variable_name)

        if not file_paths:
            return JsonResponse(
                {'error': 'No files found for the selected variable.'},
                status=404
            )

        datasets = xr.open_mfdataset(file_paths, combine='by_coords')

        actual_variable = VARIABLE_MAP.get(variable_name, variable_name)

        start_time = pd.Timestamp(start_date)
        end_time = pd.Timestamp(end_date)

        time_filtered_data = datasets[actual_variable].sel(
            valid_time=slice(start_time, end_time)
        )

        if lat and lon:
            data = time_filtered_data.sel(
                latitude=float(lat),
                longitude=float(lon),
                method="nearest"
            )

        elif coordinates:
            coords = [tuple(map(float, coord.split(',')))
                      for coord in coordinates.split(';')]

            min_lat = min(coord[0] for coord in coords)
            max_lat = max(coord[0] for coord in coords)
            min_lon = min(coord[1] for coord in coords)
            max_lon = max(coord[1] for coord in coords)

            data = time_filtered_data.sel(
                latitude=slice(min_lat, max_lat),
                longitude=slice(min_lon, max_lon)
            )

        df = data.to_dataframe().reset_index()

        df['valid_time'] = pd.to_datetime(df['valid_time'])
        df['valid_time'] = df['valid_time'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        df = df.rename(columns={"valid_time": "time"})

        return JsonResponse(df.to_dict(orient='records'), safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def download_csv(request):
    try:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        variable_name = request.GET.get('variable')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        coordinates = request.GET.get('coordinates')

        if not variable_name or not start_date or not end_date:
            return JsonResponse(
                {'error': 'Variable, start date, and end date are required.'},
                status=400
            )

        file_paths = get_file_paths(variable_name)

        if not file_paths:
            return JsonResponse(
                {'error': 'No files found for the selected variable.'},
                status=404
            )

        datasets = xr.open_mfdataset(file_paths, combine='by_coords')

        actual_variable = VARIABLE_MAP.get(variable_name, variable_name)

        start_time = pd.Timestamp(start_date)
        end_time = pd.Timestamp(end_date)

        time_filtered_data = datasets[actual_variable].sel(
            valid_time=slice(start_time, end_time)
        )

        if lat and lon:
            data = time_filtered_data.sel(
                latitude=float(lat),
                longitude=float(lon),
                method="nearest"
            )

        elif coordinates:
            coords = [tuple(map(float, coord.split(',')))
                      for coord in coordinates.split(';')]

            min_lat = min(coord[0] for coord in coords)
            max_lat = max(coord[0] for coord in coords)
            min_lon = min(coord[1] for coord in coords)
            max_lon = max(coord[1] for coord in coords)

            data = time_filtered_data.sel(
                latitude=slice(min_lat, max_lat),
                longitude=slice(min_lon, max_lon)
            )

        df = data.to_dataframe().reset_index()

        df['valid_time'] = pd.to_datetime(df['valid_time'])
        df['valid_time'] = df['valid_time'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        df = df.rename(columns={"valid_time": "time"})

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        response = HttpResponse(
            csv_buffer.getvalue(),
            content_type="text/csv"
        )

        response['Content-Disposition'] = 'attachment; filename="climate_data.csv"'

        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)