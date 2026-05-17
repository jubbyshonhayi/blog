import logging

from django.conf import settings
from django.db import InterfaceError, OperationalError
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class DatabaseUnavailableMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except (OperationalError, InterfaceError):
            if settings.DEBUG:
                raise

            logger.exception("Database is temporarily unavailable.")
            return HttpResponse(
                "Service temporarily unavailable.",
                status=503,
                content_type="text/plain",
            )
