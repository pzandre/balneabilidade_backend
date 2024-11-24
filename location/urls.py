from django.urls import path

from location.views import (
    LocationConditionCronJobAPIView,
    LocationListAPIView,
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
    path("locations/", LocationListAPIView.as_view(), name="location-list"),
    path("weather/", WeatherReportAPIView.as_view(), name="weather-report"),
]
