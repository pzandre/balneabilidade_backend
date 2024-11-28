from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

from location.models import (
    City,
    CityURL,
    Country,
    Location,
    ManagementAPIKey,
    State,
    WeatherReport,
)


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city__name", "latitude", "longitude", "is_good")
    search_fields = ("name", "city__name")
    list_filter = ("is_good",)
    list_select_related = ("city",)
    ordering = ("name",)


class ManagementAPIKeyModelAdmin(APIKeyModelAdmin):
    model = ManagementAPIKey


admin.site.register(City)
admin.site.register(CityURL)
admin.site.register(Country)
admin.site.register(Location, LocationAdmin)
admin.site.register(State)
admin.site.register(WeatherReport)
admin.site.register(ManagementAPIKey, ManagementAPIKeyModelAdmin)
