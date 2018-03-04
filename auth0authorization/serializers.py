from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Country, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('country', 'country_code')
