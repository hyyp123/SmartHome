from __future__ import unicode_literals

from django.db import models

# Create your models here.

class DevicesDbTable(models.Model):
    # deviceName=models.CharField(max_length=50)
    order=models.IntegerField(null=True)
    deviceStatus=models.IntegerField()
    raspberryId=models.IntegerField()
