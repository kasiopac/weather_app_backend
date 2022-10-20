from django.db import models
from django.contrib.auth.models import User


class MyCity(models.Model):
    user = models.ForeignKey(
        User, max_length=100, on_delete=models.CASCADE, related_name="mycity", null=True
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# not used for now
class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# not used for now
class ForecastForCity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    forecast_dt = models.DateTimeField()

    current_description = models.CharField(max_length=100)
    current_icon = models.CharField(max_length=100)
    current_rain = models.FloatField()
    current_temp = models.IntegerField()

    hourly_04_description = models.CharField(max_length=100)
    hourly_08_description = models.CharField(max_length=100)
    hourly_12_description = models.CharField(max_length=100)
    hourly_16_description = models.CharField(max_length=100)
    hourly_20_description = models.CharField(max_length=100)
    hourly_24_description = models.CharField(max_length=100)
    hourly_28_description = models.CharField(max_length=100)
    hourly_32_description = models.CharField(max_length=100)
    hourly_36_description = models.CharField(max_length=100)
    hourly_40_description = models.CharField(max_length=100)
    hourly_44_description = models.CharField(max_length=100)
    hourly_48_description = models.CharField(max_length=100)

    daily_1_description = models.CharField(max_length=100)
    daily_2_description = models.CharField(max_length=100)
    daily_3_description = models.CharField(max_length=100)
    daily_4_description = models.CharField(max_length=100)
    daily_5_description = models.CharField(max_length=100)
