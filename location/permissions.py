from rest_framework_api_key.permissions import HasAPIKey

from location.models import ManagementAPIKey


class HasManagementAPIKey(HasAPIKey):
    model = ManagementAPIKey
