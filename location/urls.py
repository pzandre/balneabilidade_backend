from django.urls import path

from location.views import (
    DumpDBCronJobAPIView,
    LocationConditionCronJobAPIView,
    LocationListAPIView,
    LocationReportDetailAPIView,
    RestoreDBAPIView,
    WeatherReportAPIView,
    WeatherReportCronJobAPIView,
)

app_name = "location"

urlpatterns = [
    path(
        "management/locations/",
        LocationConditionCronJobAPIView.as_view(),
        name="location-condition-cron-job",
    ),
    path(
        "management/weather/",
        WeatherReportCronJobAPIView.as_view(),
        name="weather-report-cron-job",
    ),
    path(
        "management/initiate_backup_process/",
        DumpDBCronJobAPIView.as_view(),
        name="dump-db-cron-job",
    ),
    path(
        "management/initiate_restore_process/",
        RestoreDBAPIView.as_view(),
        name="restore-db-api",
    ),
    path("locations/", LocationListAPIView.as_view(), name="location-list"),
    path("weather/", WeatherReportAPIView.as_view(), name="weather-report"),
    path(
        "report/", LocationReportDetailAPIView.as_view(), name="location-report-detail"
    ),
]
