import os
import re

from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.utils.cache import add_never_cache_headers


class DisableClientSideCacheMiddleware:
    """
    Middleware to disable client-side caching.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response


class VercelDynamicAllowedHostsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.vercel_host_pattern = re.compile(
            r"{}".format(os.getenv("VERCEL_HOST_PATTERN"))
        )
        self.prod_domain = os.getenv("PROD_DOMAIN")

    def __call__(self, request):
        host = request.get_host().split(":")[0]

        if (
            settings.DEBUG
            or self.prod_domain == host
            or self.vercel_host_pattern.match(host)
        ):
            return self.get_response(request)

        raise DisallowedHost(f"Disallowed host: {host}")
