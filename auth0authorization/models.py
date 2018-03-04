from django.db import models

# Create your models here.

class Country(models.Model):
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=5)

    def __str__(self):
        return country

class City(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="country_city")
    city = models.CharField(max_length=100)

    def __str__(self):
        return city
