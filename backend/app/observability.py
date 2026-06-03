"""Minimal deployment observability hooks."""

from __future__ import annotations

import json
import logging
import os
import time
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response


APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
REQUEST_ID_HEADER = "X-Request-ID"
TRACE_ID_HEADER = "X-Trace-ID"

request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)
logger = logging.getLogger("zippy.request")


def configure_logging() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())


def init_sentry_if_configured() -> None:
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        return
    try:
        import sentry_sdk  # type: ignore
    except Exception:
        logging.getLogger("zippy.observability").warning(
            "SENTRY_DSN is set but sentry_sdk is not installed; continuing without Sentry"
        )
        return
    sentry_sdk.init(dsn=dsn, traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0")))


def current_request_id() -> str | None:
    return request_id_context.get()


class RequestIdLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid4())
        trace_id = request.headers.get(TRACE_ID_HEADER) or request_id
        request.state.request_id = request_id
        request.state.trace_id = trace_id
        token = request_id_context.set(request_id)
        start = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                json.dumps(
                    {
                        "event": "http_request",
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": status_code,
                        "latency_ms": latency_ms,
                        "request_id": request_id,
                        "trace_id": trace_id,
                    },
                    separators=(",", ":"),
                )
            )
            request_id_context.reset(token)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None) or str(uuid4())
    logging.getLogger("zippy.error").exception(
        "Unhandled request error",
        extra={"request_id": request_id, "path": request.url.path, "method": request.method},
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error",
                "request_id": request_id,
            }
        },
        headers={REQUEST_ID_HEADER: request_id},
    )
