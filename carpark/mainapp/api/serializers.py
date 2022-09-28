from rest_framework import serializers

from mainapp.models import Driver
from mainapp.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    tz_info = serializers.CharField()

    class Meta:
        model = Vehicle
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
