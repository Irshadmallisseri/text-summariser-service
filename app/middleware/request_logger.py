import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.logging_config import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} [{duration}ms]"
        )

        return response