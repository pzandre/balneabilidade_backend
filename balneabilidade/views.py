from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 60 * 24 * 365, key_prefix="privacy_policy")
def privacy_policy_view(request):
    return render(request, "privacy_policy.html")
