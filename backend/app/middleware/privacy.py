"""DPDP-oriented response masking for personal contact fields."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


PHONE_FIELD_MARKERS = {
    "phone",
    "mobile",
    "contact_number",
    "contact_phone",
    "shipper_phone",
    "driver_phone",
    "consignee_phone",
}


def mask_phone_number(value: Any) -> Any:
    """Mask an Indian phone-like value while preserving last four digits."""
    if value is None:
        return value

    text = str(value)
    digits = [char for char in text if char.isdigit()]
    if len(digits) < 4:
        return "****"

    suffix = "".join(digits[-4:])
    return f"******{suffix}"


def _is_phone_key(key: str) -> bool:
    normalized = key.lower()
    return any(marker in normalized for marker in PHONE_FIELD_MARKERS)


def mask_pii_payload(payload: Any) -> Any:
    """Recursively mask phone fields in dict/list response payloads."""
    if isinstance(payload, list):
        return [mask_pii_payload(item) for item in payload]

    if isinstance(payload, Mapping):
        masked: dict[str, Any] = {}
        for key, value in payload.items():
            if _is_phone_key(str(key)):
                masked[str(key)] = mask_phone_number(value)
            else:
                masked[str(key)] = mask_pii_payload(value)
        return masked

    return payload


class DPDPPrivacyMaskingMiddleware(BaseHTTPMiddleware):
    """Masks phone numbers from JSON API responses unless explicitly bypassed.

    The bypass is intentionally narrow and header-gated so internal tests or
    privileged server-to-server calls can inspect raw data without changing
    controller behavior. Public frontend calls receive masked phone values.
    """

    bypass_header = "x-zippy-pii-access"

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        if request.headers.get(self.bypass_header, "").lower() == "full":
            return response

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        if not body:
            return Response(status_code=response.status_code, headers=dict(response.headers))

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=content_type,
            )

        headers = dict(response.headers)
        headers.pop("content-length", None)
        return JSONResponse(
            content=mask_pii_payload(payload),
            status_code=response.status_code,
            headers=headers,
        )
