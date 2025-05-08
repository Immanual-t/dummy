from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import threading

# Use thread-local storage for preserving original settings
_thread_local = threading.local()

class SeparateAdminSessionMiddleware(MiddlewareMixin):
    """
    Middleware that ensures complete separation between admin and frontend sessions
    by using different cookie names and paths.
    """

    def process_request(self, request):
        """Configure session settings based on request path"""
        # Store original settings in thread-local storage
        if not hasattr(_thread_local, 'original_settings'):
            _thread_local.original_settings = {
                'session_cookie_name': settings.SESSION_COOKIE_NAME,
                'csrf_cookie_name': settings.CSRF_COOKIE_NAME,
                'session_cookie_path': getattr(settings, 'SESSION_COOKIE_PATH', '/'),
                'csrf_cookie_path': getattr(settings, 'CSRF_COOKIE_PATH', '/')
            }

        # Mark admin requests
        is_admin = request.path.startswith('/admin/')
        request.is_admin_request = is_admin

        # Use different cookie settings based on request type
        if is_admin:
            settings.SESSION_COOKIE_NAME = 'finarva_admin_sessionid'
            settings.CSRF_COOKIE_NAME = 'finarva_admin_csrftoken'
        else:
            settings.SESSION_COOKIE_NAME = 'finarva_sessionid'
            settings.CSRF_COOKIE_NAME = 'finarva_csrftoken'

    def process_response(self, request, response):
        """Restore original settings and ensure cookies have the correct paths"""
        # Restore original settings
        if hasattr(_thread_local, 'original_settings'):
            settings.SESSION_COOKIE_NAME = _thread_local.original_settings['session_cookie_name']
            settings.CSRF_COOKIE_NAME = _thread_local.original_settings['csrf_cookie_name']
            settings.SESSION_COOKIE_PATH = _thread_local.original_settings['session_cookie_path']
            settings.CSRF_COOKIE_PATH = _thread_local.original_settings['csrf_cookie_path']

        return response