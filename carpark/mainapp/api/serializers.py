from rest_framework import serializers

from mainapp.models import Driver
from mainapp.models import Enterprise
from mainapp.models import Vehicle


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'tz_info')


class VehicleSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'cost',
            'release_date',
            'mileage',
            'created_at',
            'brand',
            'company',
            # 'company_tz',
        )


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
