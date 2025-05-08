from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse


def admin_force_logout(request):
    """Force logout and redirect to admin login"""
    # Logout the user
    logout(request)

    # Redirect to admin login
    return HttpResponseRedirect(reverse('admin:login'))