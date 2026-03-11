from django.contrib import admin
from .models import ClimateFile

@admin.register(ClimateFile)
class ClimateFileAdmin(admin.ModelAdmin):
    list_display = ('variable_name', 'file_name', 'file_path')
    list_filter = ('variable_name',)
    search_fields = ('file_name', 'variable_name')
