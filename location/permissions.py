from rest_framework_api_key.permissions import HasAPIKey

from location.models import ManagementAPIKey


class HasManagementAPIKey(HasAPIKey):
    model = ManagementAPIKey


class HasDefaultOrManagementAPIKey(HasAPIKey):
    fallback_model = ManagementAPIKey

    def has_permission(self, request, view):
        key = self.get_key(request)
        if not key:
            return False
        return self.model.objects.is_valid(key) or self.fallback_model.objects.is_valid(
            key
        )
