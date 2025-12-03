from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_GET
import logging

logger = logging.getLogger(__name__)


@require_GET
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JsonResponse({"status": "healthy", "database": "connected"})
    except Exception as e:
        logger.error("Health check failed: %s", str(e), exc_info=True)
        return JsonResponse(
            {"status": "unhealthy", "database": "disconnected"}, status=503
        )
