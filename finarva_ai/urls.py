from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin import admin_site  # Import custom admin site
from .views import admin_force_logout  # Import the view

urlpatterns = [
    # Use our custom admin site
    path('admin/force-logout/', admin_force_logout, name='admin_force_logout'),
    path('admin/', admin_site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('ai-assistant/', include('ai_assistant.urls')),
    path('', include('dashboard.urls')),  # Root redirects to dashboard
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)