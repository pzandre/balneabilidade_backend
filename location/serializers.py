from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source="name")
    description = serializers.SerializerMethodField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    is_good = serializers.BooleanField()

    def get_description(self, obj):
        if obj.is_good:
            return "Praia própria para banho"
        return "Praia imprópria para banho"


class WeatherReportSerializer(serializers.Serializer):
    temperature = serializers.DecimalField(max_digits=5, decimal_places=1)
    condition = serializers.CharField()
