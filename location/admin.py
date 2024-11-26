from django.contrib import admin

from location.models import City, CityURL, Country, Location, State, WeatherReport


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city__name", "latitude", "longitude", "is_good")
    search_fields = ("name", "city__name")
    list_filter = ("is_good",)
    list_select_related = ("city",)
    ordering = ("name",)


admin.site.register(City)
admin.site.register(CityURL)
admin.site.register(Country)
admin.site.register(Location, LocationAdmin)
admin.site.register(State)
admin.site.register(WeatherReport)
