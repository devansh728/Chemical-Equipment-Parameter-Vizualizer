from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'file', 'status', 'uploaded_at']
    list_filter = ['status', 'uploaded_at']
    search_fields = ['user__username', 'file']
    readonly_fields = ['uploaded_at']

