import threading
from django.utils.deprecation import MiddlewareMixin


class RequestMiddleware(MiddlewareMixin):
    """Middleware that stores request context in thread local storage"""

    thread_local = threading.local()

    def process_request(self, request):
        # Store admin flag on the request
        is_admin = request.path.startswith('/admin/')
        request.is_admin_request = is_admin

        # Store request in thread local storage
        RequestMiddleware.thread_local.request = request

    @classmethod
    def get_current_request(cls):
        """Get the current request from thread local storage"""
        if hasattr(cls.thread_local, 'request'):
            return cls.thread_local.request
        return None