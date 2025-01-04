from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from location.models import CityURL, Location, WeatherReport
from location.permissions import HasManagementAPIKey
from location.serializers import (
    LocationReportDetailSerializer,
    LocationSerializer,
    RestoreDBSerializer,
    WeatherReportSerializer,
)
from location.utils import (
    call_cloud_run_endpoint,
    get_and_update_location_conditions,
    update_weather_reports,
)


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


class LocationReportDetailAPIView(GenericAPIView):
    queryset = CityURL.objects.all()
    serializer_class = LocationReportDetailSerializer
    filterset_fields = ["city__name"]

    @method_decorator(cache_page(60 * 60 * 24, key_prefix="location_reports"))
    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().last()
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


# ~Cron Jobs~ #


class WeatherReportCronJobAPIView(GenericAPIView):
    queryset = WeatherReport.objects.all()
    serializer_class = WeatherReportSerializer
    permission_classes = (HasManagementAPIKey,)

    def post(self, request, *args, **kwargs):
        update_weather_reports()
        return Response(status=status.HTTP_201_CREATED)


class LocationConditionCronJobAPIView(GenericAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (HasManagementAPIKey,)

    def post(self, request, *args, **kwargs):
        get_and_update_location_conditions()
        return Response(status=status.HTTP_201_CREATED)


class DumpDBCronJobAPIView(GenericAPIView):
    queryset = Location.objects.none()
    permission_classes = (HasManagementAPIKey,)

    def post(self, request, *args, **kwargs):
        url = settings.CLOUD_RUN_ENDPOINT + "/management/initiate_backup_process"
        call_cloud_run_endpoint(url)
        return Response(status=status.HTTP_201_CREATED)


class RestoreDBAPIView(GenericAPIView):
    queryset = Location.objects.none()
    serializer_class = RestoreDBSerializer
    permission_classes = (HasManagementAPIKey,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = settings.CLOUD_RUN_ENDPOINT + "/management/initiate_restore_process"
        call_cloud_run_endpoint(url, serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
