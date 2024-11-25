from django.shortcuts import render


def privacy_policy_view(request):
    return render(request, "privacy_policy.html")
