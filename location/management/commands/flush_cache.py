from django.conf import settings
from django.core.management.base import BaseCommand
from redis import Redis


class Command(BaseCommand):
    help = (
        "Flushes the Redis cache. Optionally, you can provide a specific key to delete."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--key",
            type=str,
            help="Specify the key to delete from the cache",
        )

    def handle(self, *args, **options):
        key = options.get("key") or ""

        redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
        )
        try:
            keys = redis.keys(f"*{key}*")
            if keys:
                redis.delete(*keys)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error while clearing cache: {e}"))
        finally:
            redis.close()

        self.stdout.write(self.style.SUCCESS("Successfully flushed the cache"))
