from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from location.models import Location, WeatherReport
from location.serializers import LocationSerializer, WeatherReportSerializer
from location.utils import get_and_update_location_conditions, update_weather_reports


class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all().order_by("name")
    serializer_class = LocationSerializer
    filterset_fields = ["city__name"]

    @method_decorator(cache_page(60 * 60 * 24, key_prefix="locations"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class WeatherReportAPIView(GenericAPIView):
    queryset = WeatherReport.objects.all()
    serializer_class = WeatherReportSerializer
    filterset_fields = ["city__name"]

    @method_decorator(cache_page(60 * 60, key_prefix="weather_reports"))
    def get(self, request, *args, **kwargs):
        obj = self.filter_queryset(self.get_queryset()).last()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class WeatherReportCronJobAPIView(GenericAPIView):
    queryset = WeatherReport.objects.all()
    serializer_class = WeatherReportSerializer

    def post(self, request, *args, **kwargs):
        update_weather_reports()
        return Response(status=status.HTTP_201_CREATED)


class LocationConditionCronJobAPIView(GenericAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def post(self, request, *args, **kwargs):
        get_and_update_location_conditions()
        return Response(status=status.HTTP_201_CREATED)
