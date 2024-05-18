from django.db import models

class ScanResult(models.Model):
    device_id = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100)
    is_safe = models.BooleanField(default=True)
    scan_date = models.DateTimeField(auto_now_add=True)

class Device(models.Model):
    device_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)