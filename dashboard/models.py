from django.db import models

class SensorReading(models.Model):
    sensor_id = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    soil_moisture = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  # auto set when saved

    def __str__(self):
        return f"Sensor {self.sensor_id} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
