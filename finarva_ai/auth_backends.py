from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminBackend(ModelBackend):
    """Authentication backend specifically for admin users"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Only process admin requests
        if not request or not getattr(request, 'is_admin_request', False):
            return None

        try:
            user = User.objects.get(username=username)
            # Only authenticate staff users for admin
            if user.check_password(password) and user.is_staff:
                return user
        except User.DoesNotExist:
            return None

        return None


class FrontendBackend(ModelBackend):
    """Authentication backend for regular frontend users"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Skip processing for admin requests - let AdminBackend handle those
        if request and getattr(request, 'is_admin_request', False):
            return None

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None