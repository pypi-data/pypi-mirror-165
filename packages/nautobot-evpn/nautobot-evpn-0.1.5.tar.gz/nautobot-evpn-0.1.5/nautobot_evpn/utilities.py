from functools import wraps
from django.shortcuts import redirect


def redirect_to_referer(request):
    return redirect(request.META.get("HTTP_REFERER", "/"))
