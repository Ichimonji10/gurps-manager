"""Business logic for all URLs in the ``gurps_manager`` application."""
from django.shortcuts import render
from django.views.generic.base import View

class Index(View):
    """Handle a request for ``/``."""
    def get(self, request):
        """Return the homepage for this application."""
        return render(request, 'gurps_manager/index.html', {})
