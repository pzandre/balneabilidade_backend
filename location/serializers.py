from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    is_good = serializers.BooleanField()


class WeatherReportSerializer(serializers.Serializer):
    temperature = serializers.DecimalField(max_digits=5, decimal_places=2)
    condition = serializers.CharField()
