from django.db import models


class AbstractClearCacheMixin(models.Model):
    def clear_cache(self):
        from django.core.cache import cache

        cache.delete(self.cache_key)

    def save(self, *args, **kwargs):
        self.clear_cache()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class AbstractCreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AbstractUpdatedMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractCreatedUpdatedMixin(AbstractCreatedMixin, AbstractUpdatedMixin):
    class Meta:
        abstract = True


class Country(AbstractCreatedUpdatedMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"


class State(AbstractCreatedUpdatedMixin):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.country}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "country"], name="unique_state")
        ]


class City(AbstractCreatedUpdatedMixin):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.state}"

    class Meta:
        verbose_name_plural = "cities"
        constraints = [
            models.UniqueConstraint(fields=["name", "state"], name="unique_city")
        ]


class Location(AbstractCreatedUpdatedMixin, AbstractClearCacheMixin):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_good = models.BooleanField(default=True)

    cache_key = "locations"

    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "city"], name="unique_location")
        ]


class WeatherReport(AbstractUpdatedMixin, AbstractClearCacheMixin):
    CONDITION_CHOICES = (
        ("sunny", "sunny"),
        ("cloudy", "cloudy"),
        ("rainy", "rainy"),
        ("snowy", "snowy"),
        ("foggy", "foggy"),
    )

    city = models.OneToOneField(City, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    condition = models.CharField(max_length=6, choices=CONDITION_CHOICES)

    cache_key = "weather_reports"

    def __str__(self):
        return f"{self.city} - {self.temperature}°C - {self.condition}"
