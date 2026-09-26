# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Domain-aware exception hierarchy for the NIOS SDK."""

from __future__ import annotations

from typing import Any


class NiosError(Exception):
    """Base exception for all NIOS SDK errors."""

    def __init__(
        self,
        *,
        status_code: int | None = None,
        message: str,
        response_body: dict[str, Any] | None = None,
        wapi_code: str | None = None,
        wapi_text: str | None = None,
        request_url: str | None = None,
    ) -> None:
        """Initialize the base NIOS error.

        Args:
            status_code: HTTP status code that triggered the error, or None for
                non-HTTP errors.
            message: Human-readable error description.
            response_body: Parsed JSON response body from the WAPI, if available.
            wapi_code: WAPI-specific error code from the ``code`` field (e.g.
                ``"AdmConProhibited"``).
            wapi_text: WAPI-specific error text from the ``text`` field.
            request_url: Full URL of the request that caused the error.
        """
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        self.wapi_code = wapi_code
        self.wapi_text = wapi_text
        self.request_url = request_url
        super().__init__(message)


class NiosConnectionError(NiosError):
    """TLS failure, DNS failure, connect timeout - pre-HTTP-response errors."""


class AuthenticationError(NiosError):
    """401 - credentials rejected or session expired."""


class NotFoundError(NiosError):
    """404 - object does not exist."""


class BadRequestError(NiosError):
    """400 - malformed request or invalid field values."""


class ConflictError(NiosError):
    """409 - object already exists or state conflict."""


class RateLimitError(NiosError):
    """429 - too many requests."""

    def __init__(
        self,
        *,
        status_code: int | None = None,
        message: str,
        response_body: dict[str, Any] | None = None,
        wapi_code: str | None = None,
        wapi_text: str | None = None,
        request_url: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        """Initialize a rate-limit error with optional retry delay.

        Args:
            status_code: HTTP status code (typically 429).
            message: Human-readable error description.
            response_body: Parsed JSON response body from the WAPI, if available.
            wapi_code: WAPI-specific error code from the ``code`` field.
            wapi_text: WAPI-specific error text from the ``text`` field.
            request_url: Full URL of the request that caused the error.
            retry_after: Seconds to wait before retrying, parsed from the
                ``Retry-After`` response header. None if the header was absent.
        """
        super().__init__(
            status_code=status_code,
            message=message,
            response_body=response_body,
            wapi_code=wapi_code,
            wapi_text=wapi_text,
            request_url=request_url,
        )
        self.retry_after = retry_after


class ServerError(NiosError):
    """5xx - server-side failure."""


class ValidationError(NiosError):
    """Pydantic parse failure - response did not match the expected model."""


class UnsupportedOperationError(NiosError):
    """Object type does not support the requested operation - raised before the request.

    NIOS restricts some operations per object type: ``allrecords`` is a read-only
    aggregate, ``grid`` cannot be deleted, ``dtc`` accepts only function calls.
    The grid answers those with ``AdmConProtoError: Operation <op> not allowed
    for <type>``; the SDK raises this instead, from the restriction table in
    :mod:`ibx_nios_sdk._restrictions`.

    Pass ``enforce_restrictions=False`` to :class:`~ibx_nios_sdk.client.NiosClient`
    to skip the local check and let the grid decide - useful on a NIOS version
    whose restrictions differ from the table's.
    """

    def __init__(self, *, wapi_type: str, operation: str) -> None:
        """Initialize the error for one object type and operation.

        Args:
            wapi_type: WAPI object type that refused the operation.
            operation: Operation name - ``read``, ``create``, ``update``, or
                ``delete``.
        """
        self.wapi_type = wapi_type
        self.operation = operation
        super().__init__(
            message=(
                f"WAPI object type {wapi_type!r} does not support {operation}; "
                "pass enforce_restrictions=False to NiosClient to try anyway"
            )
        )


_STATUS_MAP: dict[int, type[NiosError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    404: NotFoundError,
    409: ConflictError,
    429: RateLimitError,
}


def _extract_wapi_fields(body: dict[str, Any] | None) -> tuple[str | None, str | None]:
    """Extract WAPI ``code`` and ``text`` fields from a parsed response body.

    Args:
        body: Parsed JSON response dict, or None.

    Returns:
        A ``(wapi_code, wapi_text)`` tuple; both elements are None when
        ``body`` is not a dict or the keys are absent.
    """
    if not isinstance(body, dict):
        return None, None
    return body.get("code"), body.get("text")


def exception_for_status(
    status_code: int,
    message: str,
    response_body: dict[str, Any] | None,
    *,
    retry_after: float | None = None,
    request_url: str | None = None,
) -> NiosError:
    """Create the appropriate exception for an HTTP status code.

    Maps well-known WAPI status codes to specific exception subclasses (e.g.
    401 to ``AuthenticationError``, 429 to ``RateLimitError``). Codes in the
    500–599 range produce ``ServerError``; all other unrecognised codes produce
    the base ``NiosError``.

    Args:
        status_code: HTTP response status code.
        message: Human-readable error message extracted from the response.
        response_body: Parsed JSON response body, or None.
        retry_after: Seconds to wait before retrying; used only for 429
            responses where a ``Retry-After`` header was present.
        request_url: Full URL of the request that triggered the error.

    Returns:
        A ``NiosError`` subclass instance matching the status code.
    """
    wapi_code, wapi_text = _extract_wapi_fields(response_body)

    exc_class = _STATUS_MAP.get(status_code)
    if exc_class is None:
        if 500 <= status_code < 600:
            exc_class = ServerError
        else:
            return NiosError(
                status_code=status_code,
                message=message,
                response_body=response_body,
                wapi_code=wapi_code,
                wapi_text=wapi_text,
                request_url=request_url,
            )

    if exc_class is RateLimitError:
        return RateLimitError(
            status_code=status_code,
            message=message,
            response_body=response_body,
            wapi_code=wapi_code,
            wapi_text=wapi_text,
            request_url=request_url,
            retry_after=retry_after,
        )

    return exc_class(
        status_code=status_code,
        message=message,
        response_body=response_body,
        wapi_code=wapi_code,
        wapi_text=wapi_text,
        request_url=request_url,
    )
