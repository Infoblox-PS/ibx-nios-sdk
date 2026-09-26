# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# src/ibx_nios_sdk/_http.py
"""HTTP client for Infoblox NIOS WAPI, built on httpx.AsyncClient."""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import Any

import httpx

from ibx_nios_sdk._exceptions import NiosConnectionError, exception_for_status
from ibx_nios_sdk._version import DEFAULT_WAPI_VERSION, __version__

logger = logging.getLogger("ibx_nios_sdk")

_log_level = os.environ.get("IB_LOG_LEVEL", "").upper()
if _log_level == "DEBUG":  # pragma: no cover
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)


def _is_tls_error(exc: httpx.ConnectError) -> bool:
    """Return True if a ConnectError looks like a TLS/SSL failure.

    Args:
        exc: The ``httpx.ConnectError`` to inspect.

    Returns:
        True when the exception message contains ``ssl``, ``certificate``, or
        ``tls`` (case-insensitive); False otherwise.
    """
    msg = str(exc).lower()
    return "ssl" in msg or "certificate" in msg or "tls" in msg


_RETRYABLE_STATUSES: frozenset[int] = frozenset({429, 502, 503, 504})


def _parse_retry_after(response: httpx.Response) -> float | None:
    """Parse the ``Retry-After`` header from an HTTP response.

    Args:
        response: The HTTP response to inspect.

    Returns:
        The number of seconds to wait as a float, or None if the header is
        absent or cannot be parsed as a number.
    """
    ra = response.headers.get("Retry-After")
    if not ra:
        return None
    try:
        return float(ra)
    except ValueError:
        return None


def unwrap_value(data: dict[str, Any] | None) -> Any:
    """Undo ``_safe_json``'s ``{"_value": ...}`` wrapping for non-dict bodies.

    Returns the inner payload (list/scalar) if the dict has exactly one key
    ``_value``; otherwise returns ``data`` unchanged. ``None`` stays ``None``.
    """
    if data is None:
        return None
    if tuple(data) == ("_value",):
        return data["_value"]
    return data


def _safe_json(response: httpx.Response) -> dict[str, Any] | None:
    """Attempt to parse an HTTP response body as JSON, never raising.

    Non-dict JSON values (arrays, scalars) are wrapped in ``{"_value": ...}``
    so callers always receive a dict-or-None.

    Args:
        response: The HTTP response whose body is to be parsed.

    Returns:
        The parsed JSON body as a dict, a synthetic ``{"_value": ...}`` wrapper
        for non-dict JSON, or None if the body is empty or not valid JSON.
    """
    try:
        parsed = response.json()
    except Exception:
        return None
    if isinstance(parsed, dict):
        return parsed
    return {"_value": parsed}


class HttpClient:
    """Async HTTP client for Infoblox NIOS WAPI.

    Wraps ``httpx.AsyncClient`` with WAPI-specific behaviour: session-cookie
    auth (or Basic-auth fallback), automatic retry with exponential backoff on
    429/5xx responses, one-shot 401 re-login, and structured error mapping via
    :func:`~ibx_nios_sdk._exceptions.exception_for_status`.
    """

    def __init__(
        self,
        *,
        grid_url: str,
        username: str,
        password: str,
        wapi_version: str = DEFAULT_WAPI_VERSION,
        use_session: bool = True,
        verify: bool | str | Path = True,
        timeout: float = 30.0,
        max_retries: int = 3,
        enforce_restrictions: bool = True,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Initialize the NIOS HTTP client.

        Args:
            grid_url: Base URL of the NIOS Grid Manager (e.g.
                ``"https://192.168.1.2"``). Trailing slashes are stripped.
            username: WAPI username for authentication.
            password: WAPI password for authentication.
            wapi_version: WAPI version string appended to the base URL (e.g.
                ``"2.14"`` → ``/wapi/v2.14/``).
            use_session: When True, authenticates via a WAPI session cookie
                (``GET /grid/session``). When False, sends HTTP Basic Auth on
                every request instead.
            verify: TLS certificate verification. Pass ``True`` (default) to
                verify using the system CA bundle, ``False`` to disable
                verification, or a path string to a custom CA bundle PEM file.
            timeout: Request timeout in seconds applied to all operations.
            max_retries: Maximum number of additional attempts after the first
                failure for retryable status codes (429, 502, 503, 504).
            enforce_restrictions: When True (default), resources refuse
                read/create/update/delete on object types whose WAPI schema
                restricts them, raising ``UnsupportedOperationError`` without a
                request. Set False to send the request and let the grid decide.
            transport: Custom ``httpx.AsyncBaseTransport`` for testing or
                proxying. Passed directly to ``httpx.AsyncClient``.
        """
        self._grid_url = grid_url.rstrip("/")
        self._username = username
        self._password = password
        self._wapi_version = wapi_version
        self._use_session = use_session
        self._max_retries = max_retries
        #: Whether resources gate operations on the WAPI restriction table.
        self.enforce_restrictions = enforce_restrictions
        self._logged_in = False

        client_kwargs: dict[str, Any] = {
            "base_url": f"{self._grid_url}/wapi/v{wapi_version}",
            "timeout": timeout,
            "verify": verify,
            "headers": {
                "Content-Type": "application/json",
                "x-infoblox-client": "ibx-nios-sdk",
                "x-infoblox-sdk": f"python/{__version__}",
            },
        }
        if not use_session:
            client_kwargs["auth"] = httpx.BasicAuth(username, password)
        if transport is not None:
            client_kwargs["transport"] = transport

        self._client = httpx.AsyncClient(**client_kwargs)

    @property
    def grid_url(self) -> str:
        """Base URL of the NIOS Grid Manager, without a trailing slash."""
        return self._grid_url

    async def _login(self) -> None:
        """Open a WAPI session by authenticating against the WAPI root.

        NIOS WAPI has no dedicated session-login endpoint. Any authenticated
        request to a valid WAPI path returns a ``Set-Cookie: ibapauth=...``
        header, which httpx stores in its cookie jar and reuses automatically
        on subsequent requests. This method issues ``GET /?_schema=1`` - a
        cheap, universally-supported call - purely to establish the cookie.

        Raises:
            NiosConnectionError: If the connection fails or TLS verification
                fails before a response is received.
            AuthenticationError: If the server returns 401 (bad credentials).
        """
        logger.debug("Logging in to %s", self._grid_url)
        try:
            response = await self._client.get(
                "/?_schema=1",
                auth=httpx.BasicAuth(self._username, self._password),
            )
        except httpx.ConnectError as exc:
            if _is_tls_error(exc):
                raise NiosConnectionError(
                    message=(
                        f"TLS verification failed against {self._grid_url}. "
                        "For self-signed certs, pass verify=False or "
                        "ca_bundle=/path/to/ca.pem. "
                        f"Underlying error: {exc}"
                    ),
                ) from exc
            raise NiosConnectionError(
                message=f"Connection failed to {self._grid_url}: {exc}",
            ) from exc
        if response.status_code == 401:
            raise exception_for_status(
                401,
                "NIOS login failed: bad credentials",
                _safe_json(response),
                request_url=str(response.request.url),
            )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise NiosConnectionError(
                message=(
                    f"NIOS login failed against {self._grid_url}: "
                    f"HTTP {response.status_code} at {response.request.url}"
                ),
            ) from exc
        self._logged_in = True

    async def _logout(self) -> None:
        """Invalidate the WAPI session server-side.

        Posts to ``/logout`` to expire the session cookie. Errors are silently
        swallowed so that ``aclose`` always completes cleanly.
        """
        try:
            await self._client.post("/logout")
        except Exception:
            pass
        self._logged_in = False

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Send a WAPI request with lazy login, retry, and one-shot 401 re-login.

        If ``use_session`` is True and no session exists, authenticates first.
        Retries on 429/5xx status codes up to ``max_retries`` times. On a 401
        after a successful login, re-authenticates once and retries.

        Args:
            method: HTTP method string (e.g. ``"GET"``, ``"POST"``).
            path: WAPI endpoint path relative to ``/wapi/v{version}/``. A
                leading slash is added automatically if absent.
            params: Optional query-string parameters.
            json: Optional JSON request body.

        Returns:
            The parsed JSON response body as a dict, or None for 204 responses.

        Raises:
            NiosConnectionError: If the connection fails before a response is
                received.
            NiosError: Or a subclass for non-success status codes.
        """
        if self._use_session and not self._logged_in:
            await self._login()

        url = path if path.startswith("/") else f"/{path}"
        response = await self._request_with_retry(method, url, params=params, json=json)

        if (
            self._use_session
            and response.status_code == 401
            and self._logged_in
            and not url.endswith("/grid/session")
        ):
            logger.debug("401 on %s - re-logging in", url)
            self._logged_in = False
            await self._login()
            response = await self._request_with_retry(method, url, params=params, json=json)

        return self._handle_response(response)

    async def get(
        self, path: str, *, params: dict[str, str] | None = None
    ) -> dict[str, Any] | None:
        """Send a GET request.

        Args:
            path: WAPI endpoint path relative to the base URL.
            params: Optional query-string parameters.

        Returns:
            The parsed JSON response body, or None for empty responses.

        Raises:
            NiosConnectionError: If the connection fails before a response.
            NiosError: Or a subclass for non-success status codes.
        """
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Send a POST request.

        Args:
            path: WAPI endpoint path relative to the base URL.
            params: Optional query-string parameters (e.g. ``_function``).
            json: Optional JSON request body.

        Returns:
            The parsed JSON response body, or None for empty responses.

        Raises:
            NiosConnectionError: If the connection fails before a response.
            NiosError: Or a subclass for non-success status codes.
        """
        return await self.request("POST", path, params=params, json=json)

    async def put(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Send a PUT request.

        Args:
            path: WAPI endpoint path relative to the base URL.
            params: Optional query-string parameters (e.g. ``_return_fields``).
            json: Optional JSON request body with the full resource
                representation.

        Returns:
            The parsed JSON response body, or None for empty responses.

        Raises:
            NiosConnectionError: If the connection fails before a response.
            NiosError: Or a subclass for non-success status codes.
        """
        return await self.request("PUT", path, params=params, json=json)

    async def delete(
        self, path: str, *, params: dict[str, str] | None = None
    ) -> dict[str, Any] | None:
        """Send a DELETE request.

        WAPI DELETE responses return the deleted object's ``_ref`` as a plain
        string, which ``_safe_json`` wraps as ``{"_value": ref}``.

        Args:
            path: WAPI endpoint path relative to the base URL.
            params: Optional query-string parameters.

        Returns:
            The parsed JSON response body (typically ``{"_value": ref}``), or
            None for empty responses.

        Raises:
            NiosConnectionError: If the connection fails before a response.
            NiosError: Or a subclass for non-success status codes.
        """
        return await self.request("DELETE", path, params=params)

    async def get_with_return_fields(
        self,
        path: str,
        *,
        model_fields: list[str],
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
        extra_params: dict[str, str] | None = None,
    ) -> dict[str, Any] | None:
        """Send a GET request with ``_return_fields`` / ``_return_fields+`` merged in.

        Delegates field selection logic to
        :func:`~ibx_nios_sdk._query.build_return_fields_params`.

        Args:
            path: WAPI endpoint path relative to the base URL.
            model_fields: Fields defined on the SDK model - used as the default
                set when neither ``return_fields`` nor ``return_fields_plus`` is
                provided.
            return_fields: Exact list of fields to request; mutually exclusive
                with ``return_fields_plus``.
            return_fields_plus: Additional fields to append to ``model_fields``;
                mutually exclusive with ``return_fields``.
            extra_params: Additional query-string parameters merged after field
                params (e.g. ``{"_return_as_object": "1"}``).

        Returns:
            The parsed JSON response body, or None for empty responses.

        Raises:
            ValueError: If both ``return_fields`` and ``return_fields_plus``
                are provided.
            NiosConnectionError: If the connection fails before a response.
            NiosError: Or a subclass for non-success status codes.
        """
        from ibx_nios_sdk._query import build_return_fields_params

        params = build_return_fields_params(
            model_fields=model_fields,
            return_fields=return_fields,
            return_fields_plus=return_fields_plus,
        )
        if extra_params:
            params.update(extra_params)
        return await self.request("GET", path, params=params or None)

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Execute an HTTP request with exponential-backoff retry on transient errors.

        Retries on status codes in ``_RETRYABLE_STATUSES`` (429, 502, 503, 504)
        up to ``max_retries`` additional times. Honours the ``Retry-After``
        header when present; otherwise uses exponential back-off capped at 30 s.

        Args:
            method: HTTP method string (e.g. ``"GET"``).
            url: Absolute or relative URL path accepted by the underlying client.
            params: Optional query-string parameters.
            json: Optional JSON request body.

        Returns:
            The final ``httpx.Response`` - either a success or the last
            retryable failure after all attempts are exhausted.
        """
        for attempt in range(1 + self._max_retries):
            response = await self._send(method, url, params=params, json=json)
            if response.status_code not in _RETRYABLE_STATUSES or attempt >= self._max_retries:
                return response

            delay = _parse_retry_after(response)
            if delay is None or delay <= 0:
                delay = min(2**attempt * 0.5, 30.0)

            logger.debug(
                "Retrying %s %s (attempt %d/%d, status %d, delay %.1fs)",
                method,
                url,
                attempt + 1,
                self._max_retries,
                response.status_code,
                delay,
            )
            await asyncio.sleep(delay)

        raise AssertionError("unreachable")  # pragma: no cover

    async def _send(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """Dispatch a single HTTP request to the underlying ``httpx.AsyncClient``.

        Translates ``httpx.ConnectError`` into ``NiosConnectionError`` with a
        human-readable message that distinguishes TLS failures from general
        connectivity problems.

        Args:
            method: HTTP method string (e.g. ``"GET"``).
            url: Path appended to the client's ``base_url``.
            params: Optional query-string parameters.
            json: Optional JSON request body.

        Returns:
            The raw ``httpx.Response`` from the server.

        Raises:
            NiosConnectionError: If the network connection or TLS handshake
                fails before any response is received.
        """
        logger.debug("%s %s%s params=%s", method, self._client.base_url, url, params)
        try:
            return await self._client.request(method, url, params=params, json=json)
        except httpx.ConnectError as exc:
            if _is_tls_error(exc):
                raise NiosConnectionError(
                    message=(
                        f"TLS verification failed against {self._grid_url}. "
                        "For self-signed certs, pass verify=False or "
                        "ca_bundle=/path/to/ca.pem. "
                        f"Underlying error: {exc}"
                    ),
                ) from exc
            raise NiosConnectionError(
                message=f"Connection failed to {self._grid_url}: {exc}",
            ) from exc

    def _handle_response(self, response: httpx.Response) -> dict[str, Any] | None:
        """Process an HTTP response, returning parsed JSON or raising on error.

        Args:
            response: The HTTP response to process.

        Returns:
            The parsed JSON body as a dict, or None for 204 No Content
            responses.

        Raises:
            NiosError: Or a subclass for non-success status codes, with the
                WAPI ``Error`` or ``text`` field used as the error message when
                available.
        """
        if response.status_code == 204:
            return None

        body = _safe_json(response)

        if response.is_success:
            return body

        message = (
            _extract_error_message(body)
            or response.reason_phrase
            or f"HTTP {response.status_code}"
        )
        raise exception_for_status(
            response.status_code,
            message,
            body,
            request_url=str(response.request.url),
        )

    async def aclose(self) -> None:
        """Close the client, logging out of any active WAPI session first.

        If a session cookie is active, calls ``_logout`` to invalidate it
        server-side before closing the underlying ``httpx.AsyncClient``.

        Example:
            Explicit close::

                client = HttpClient(grid_url=..., username=..., password=...)
                try:
                    ...
                finally:
                    await client.aclose()
        """
        if self._use_session and self._logged_in:
            await self._logout()
        await self._client.aclose()


def _extract_error_message(body: dict[str, Any] | None) -> str | None:
    """Extract a human-readable error string from a WAPI error response body.

    WAPI error responses typically have the shape
    ``{"Error": "...", "code": "...", "text": "..."}``. This function tries
    ``Error`` first, then falls back to ``text``.

    Args:
        body: Parsed JSON response dict, or None.

    Returns:
        The error string, or None if ``body`` is not a dict or neither key is
        present as a string value.
    """
    if not isinstance(body, dict):
        return None
    # WAPI standard error shape: {"Error": "...", "code": "...", "text": "..."}
    err = body.get("Error") or body.get("text")
    if isinstance(err, str):
        return err
    return None
