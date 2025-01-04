from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@cache_page(60 * 60 * 24 * 7, key_prefix="privacy_policy")
def privacy_policy_view(request):
    return render(request, "privacy_policy.html")


@cache_page(60 * 60 * 24 * 7, key_prefix="terms_of_service")
def terms_of_service_view(request):
    return render(request, "terms_of_service.html")


class HealthCheckView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data={"status": "ok"})
