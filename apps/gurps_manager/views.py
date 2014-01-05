"""Business logic for all URLs in the ``gurps_manager`` application."""
from django import http
from django.shortcuts import render

def index(request):
    """Handle a request for ``/``."""
    def get_handler():
        """Return the homepage for this application."""
        return render(request, 'gurps_manager/index.html', {})

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

def _http_405():
    """Return an ``HttpResponse`` with a 405 status code."""
    return http.HttpResponse(status = 405)

def _request_type(request):
    """Determine what HTTP method ``request.method`` represents.

    ``request`` is a ``django.http.HttpRequest`` object.

    If ``request`` is an HTTP POST request and '_method' is a query string key,
    return the corresponding value. Otherwise, return ``request.method``.

    """
    method = request.method
    if 'POST' == method:
        return request.POST.get('_method', 'POST')
    return method
