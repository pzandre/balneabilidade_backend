import logging

from django.conf import settings
from django.db import models
from redis import Redis


class AbstractClearCacheMixin(models.Model):
    def clear_cache(self):
        redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
        )
        try:
            keys = redis.keys(f"*{self.cache_key}*")
            if not keys:
                return
            redis.delete(*keys)
        except Exception as e:
            logging.error(f"Error while clearing cache: {e}")
        finally:
            redis.close()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clear_cache()

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


class CityURL(AbstractCreatedUpdatedMixin):
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    query_url = models.URLField()
    posted_at = models.DateField()
    url = models.URLField()

    def __str__(self):
        return f"{self.city} - {self.url}"
