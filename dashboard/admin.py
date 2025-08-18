from django.contrib import admin
from .models import SensorReading

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'temperature', 'humidity', 'soil_moisture', 'timestamp')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
