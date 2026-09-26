# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# src/ibx_nios_sdk/client.py
"""NiosClient - top-level entry point for the SDK."""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from functools import cached_property
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Any

import httpx

from ibx_nios_sdk._exceptions import NiosError
from ibx_nios_sdk._http import HttpClient, unwrap_value
from ibx_nios_sdk._version import DEFAULT_WAPI_VERSION

_FALSY_ENV = frozenset({"false", "0", "no"})
_WAPI_OBJECT_TYPE = re.compile(r"[a-z][a-z0-9_-]*(?::[a-z][a-z0-9_-]*)*")
_SECRET_PARAMETER_NAMES = frozenset(
    {
        "accesstoken",
        "apikey",
        "authorization",
        "authtoken",
        "bearertoken",
        "clientsecret",
        "credential",
        "credentials",
        "idtoken",
        "passphrase",
        "passwd",
        "password",
        "refreshtoken",
        "secret",
        "sessiontoken",
        "token",
    }
)


def _validate_wapi_object_type(object_type: str) -> None:
    """Reject anything other than a single WAPI collection object type."""
    if not isinstance(object_type, str) or _WAPI_OBJECT_TYPE.fullmatch(object_type) is None:
        raise ValueError(
            "WAPI object type must be a lowercase collection name without a URL, path, or query"
        )


def _validate_safe_read_params(params: Mapping[str, str] | None) -> None:
    """Reject query parameter names commonly used to carry credentials."""
    if params is None:
        return
    for name, value in params.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise ValueError("Raw read parameters must contain only string names and values")
        normalized_name = "".join(
            character for character in name.casefold() if character.isalnum()
        )
        if normalized_name in _SECRET_PARAMETER_NAMES:
            raise ValueError("Raw reads do not accept secret-bearing parameter names")


def _resolve_verify(
    verify: bool | str | Path,
    ca_bundle: str | Path | None,
    env_verify: str | None,
) -> bool | str:
    """Resolve the TLS verify argument for httpx from explicit and env inputs.

    Precedence: ``ca_bundle`` > explicit ``verify`` > ``NIOS_VERIFY`` env var.
    Exposed for tests; used by NiosClient during construction.
    """
    if ca_bundle is not None:
        return str(ca_bundle)
    if verify is True and env_verify is not None and env_verify.lower() in _FALSY_ENV:
        return False
    return verify if isinstance(verify, bool) else str(verify)


if TYPE_CHECKING:
    from ibx_nios_sdk.acl import AclService
    from ibx_nios_sdk.cloud import CloudService
    from ibx_nios_sdk.dhcp import DhcpService
    from ibx_nios_sdk.discovery import DiscoveryService
    from ibx_nios_sdk.dns import DnsService
    from ibx_nios_sdk.dtc import DtcService
    from ibx_nios_sdk.federatedrealms import FederatedrealmsService
    from ibx_nios_sdk.grid import GridService
    from ibx_nios_sdk.ipam import IpamService
    from ibx_nios_sdk.microsoftserver import MicrosoftserverService
    from ibx_nios_sdk.misc import MiscService
    from ibx_nios_sdk.notification import NotificationService
    from ibx_nios_sdk.rpz import RpzService
    from ibx_nios_sdk.security import SecurityService
    from ibx_nios_sdk.smartfolder import SmartfolderService
    from ibx_nios_sdk.threatinsight import ThreatinsightService
    from ibx_nios_sdk.threatprotection import ThreatprotectionService


class NiosClient:
    """Entry point for the Infoblox NIOS SDK.

    Per-domain services (``dns``, ``dhcp``, ``ipam``, ...) are exposed as
    ``@cached_property`` attributes and lazily instantiated on first access.
    The client supports use as an async context manager and reads configuration
    from environment variables when constructor arguments are omitted.

    Environment variables:

    - ``NIOS_GRID_URL``: Fallback for ``grid_url``.
    - ``NIOS_USERNAME``: Fallback for ``username``.
    - ``NIOS_PASSWORD``: Fallback for ``password``.
    - ``NIOS_WAPI_VERSION``: Fallback for ``wapi_version``.

    Example:
        Use as an async context manager::

            async with NiosClient(
                grid_url="https://192.168.1.2",
                username="admin",
                password="secret",
            ) as client:
                records = await client.dns.a_record.list(name="host.example.com").all()
    """

    def __init__(
        self,
        *,
        grid_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        wapi_version: str | None = None,
        use_session: bool = True,
        verify: bool | str | Path = True,
        ca_bundle: str | Path | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        enforce_restrictions: bool = True,
        _transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Initialize the NIOS client.

        Args:
            grid_url: Base URL of the NIOS Grid Manager (e.g.
                ``"https://192.168.1.2"``). Falls back to the
                ``NIOS_GRID_URL`` environment variable.
            username: WAPI username. Falls back to ``NIOS_USERNAME``.
            password: WAPI password. Falls back to ``NIOS_PASSWORD``.
            wapi_version: WAPI version string (e.g. ``"2.14"``). Falls back to
                ``NIOS_WAPI_VERSION``, then the SDK default. The SDK's hand-
                written pydantic models, readonly/create-only sets, default
                return-field lists, and Literal enum types are calibrated
                against NIOS **v2.14**. Pointing at an older grid may work for
                reads (optional fields tolerate absence) but list/get requests
                can fail with ``AdmConProtoError: Unknown argument`` because
                the SDK requests return-fields the older schema does not know.
                Mitigations: pass ``return_fields=[...]`` explicitly on each
                call, or pin this SDK to a release aligned with your grid
                version.
            use_session: When True (default), authenticates via a session cookie
                from ``GET /grid/session``. When False, sends Basic Auth on
                every request.
            verify: TLS certificate verification. Pass ``True`` to verify with
                the system CA bundle, ``False`` to disable, or a path string to
                a custom CA bundle PEM file.
            ca_bundle: Convenience alias for a custom CA bundle path. When set,
                overrides ``verify`` with ``str(ca_bundle)``.
            timeout: Request timeout in seconds for all WAPI calls.
            max_retries: Number of additional retry attempts on 429/5xx
                responses.
            enforce_restrictions: When True (default), a resource method raises
                :class:`~ibx_nios_sdk._exceptions.UnsupportedOperationError`
                instead of calling WAPI for an operation the object type's
                schema restricts - ``create`` on the read-only ``allrecords``
                aggregate, ``delete`` on the ``grid`` singleton, or any read of
                a function-only type such as ``dtc``. The table is recorded from
                NIOS 9.1 / WAPI 2.14; set this False on a grid whose
                restrictions differ, and let the grid reject the call instead.
            _transport: Custom ``httpx.AsyncBaseTransport`` for testing.
                Not intended for production use.

        Raises:
            NiosError: If ``grid_url`` is not provided and ``NIOS_GRID_URL`` is
                not set, or if ``username``/``password`` are absent.
        """
        grid_url = grid_url or os.environ.get("NIOS_GRID_URL")
        username = username or os.environ.get("NIOS_USERNAME")
        password = password or os.environ.get("NIOS_PASSWORD")
        wapi_version = wapi_version or os.environ.get("NIOS_WAPI_VERSION") or DEFAULT_WAPI_VERSION

        if not grid_url:
            raise NiosError(message="grid_url is required (set arg or NIOS_GRID_URL env var)")
        if not username or not password:
            raise NiosError(
                message="credentials are required (pass username/password or set NIOS_USERNAME/NIOS_PASSWORD)"
            )

        verify = _resolve_verify(verify, ca_bundle, os.environ.get("NIOS_VERIFY"))

        self._http = HttpClient(
            grid_url=grid_url,
            username=username,
            password=password,
            wapi_version=wapi_version,
            use_session=use_session,
            verify=verify,
            timeout=timeout,
            max_retries=max_retries,
            enforce_restrictions=enforce_restrictions,
            transport=_transport,
        )

    @property
    def grid_url(self) -> str:
        """Base URL of the NIOS Grid Manager, without a trailing slash."""
        return self._http.grid_url

    async def read_raw(
        self,
        object_type: str,
        *,
        params: Mapping[str, str] | None = None,
    ) -> Any:
        """Read an uncoerced WAPI collection or its schema through SDK transport.

        This narrow fallback accepts only a single WAPI object type. Schema and
        paging controls must be supplied through ``params``; URLs, object refs,
        embedded query strings, and credential-bearing parameters are rejected.
        Prefer the typed resource APIs whenever one is available.
        """
        _validate_wapi_object_type(object_type)
        _validate_safe_read_params(params)
        result = await self._http.get(object_type, params=dict(params) if params else None)
        return unwrap_value(result)

    async def read_schema(self, object_type: str | None = None) -> Any:
        """Read the WAPI root schema or one collection object's schema.

        Args:
            object_type: A safe WAPI collection object type. When omitted, the
                WAPI version root schema is returned.

        Returns:
            The uncoerced JSON schema response from NIOS.

        Raises:
            ValueError: If ``object_type`` is not a safe collection name.
            NiosError: Or a subclass for transport or WAPI errors.
        """
        if object_type is not None:
            _validate_wapi_object_type(object_type)
        result = await self._http.get(object_type or "/", params={"_schema": "1"})
        return unwrap_value(result)

    @cached_property
    def acl(self) -> AclService:
        """Entry point for NIOS Access Control List resources."""
        from ibx_nios_sdk.acl import AclService

        return AclService(self._http)

    @cached_property
    def cloud(self) -> CloudService:
        """Entry point for NIOS Cloud resources."""
        from ibx_nios_sdk.cloud import CloudService

        return CloudService(self._http)

    @cached_property
    def discovery(self) -> DiscoveryService:
        """Entry point for NIOS Discovery resources."""
        from ibx_nios_sdk.discovery import DiscoveryService

        return DiscoveryService(self._http)

    @cached_property
    def microsoftserver(self) -> MicrosoftserverService:
        """Entry point for NIOS Microsoft Server resources."""
        from ibx_nios_sdk.microsoftserver import MicrosoftserverService

        return MicrosoftserverService(self._http)

    @cached_property
    def federatedrealms(self) -> FederatedrealmsService:
        """Entry point for NIOS Federated Realms resources."""
        from ibx_nios_sdk.federatedrealms import FederatedrealmsService

        return FederatedrealmsService(self._http)

    @cached_property
    def misc(self) -> MiscService:
        """Entry point for miscellaneous NIOS WAPI resources."""
        from ibx_nios_sdk.misc import MiscService

        return MiscService(self._http)

    @cached_property
    def notification(self) -> NotificationService:
        """Entry point for NIOS Notification resources."""
        from ibx_nios_sdk.notification import NotificationService

        return NotificationService(self._http)

    @cached_property
    def smartfolder(self) -> SmartfolderService:
        """Entry point for NIOS Smart Folder resources."""
        from ibx_nios_sdk.smartfolder import SmartfolderService

        return SmartfolderService(self._http)

    @cached_property
    def dtc(self) -> DtcService:
        """Entry point for NIOS DNS Traffic Control resources."""
        from ibx_nios_sdk.dtc import DtcService

        return DtcService(self._http)

    @cached_property
    def dhcp(self) -> DhcpService:
        """Entry point for NIOS DHCP resources."""
        from ibx_nios_sdk.dhcp import DhcpService

        return DhcpService(self._http)

    @cached_property
    def dns(self) -> DnsService:
        """Entry point for NIOS DNS resources."""
        from ibx_nios_sdk.dns import DnsService

        return DnsService(self._http)

    @cached_property
    def grid(self) -> GridService:
        """Entry point for NIOS Grid resources."""
        from ibx_nios_sdk.grid import GridService

        return GridService(self._http)

    @cached_property
    def ipam(self) -> IpamService:
        """Entry point for NIOS IPAM resources."""
        from ibx_nios_sdk.ipam import IpamService

        return IpamService(self._http)

    @cached_property
    def rpz(self) -> RpzService:
        """Entry point for NIOS Response Policy Zone resources."""
        from ibx_nios_sdk.rpz import RpzService

        return RpzService(self._http)

    @cached_property
    def security(self) -> SecurityService:
        """Entry point for NIOS Security resources."""
        from ibx_nios_sdk.security import SecurityService

        return SecurityService(self._http)

    @cached_property
    def threatinsight(self) -> ThreatinsightService:
        """Entry point for NIOS Threat Insight resources."""
        from ibx_nios_sdk.threatinsight import ThreatinsightService

        return ThreatinsightService(self._http)

    @cached_property
    def threatprotection(self) -> ThreatprotectionService:
        """Entry point for NIOS Threat Protection resources."""
        from ibx_nios_sdk.threatprotection import ThreatprotectionService

        return ThreatprotectionService(self._http)

    async def aclose(self) -> None:
        """Close the underlying HTTP client and release any active WAPI session.

        Calls :meth:`~ibx_nios_sdk._http.HttpClient.aclose`, which logs out of
        the WAPI session if one is active before closing the ``httpx.AsyncClient``.

        Example:
            Explicit lifecycle management::

                client = NiosClient(grid_url=..., username=..., password=...)
                try:
                    ...
                finally:
                    await client.aclose()
        """
        await self._http.aclose()

    async def __aenter__(self) -> NiosClient:
        """Enter the async context manager.

        Returns:
            This :class:`NiosClient` instance.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Exit the async context manager and close the client.

        Args:
            exc_type: Exception type, if an exception occurred.
            exc: Exception instance, if an exception occurred.
            tb: Traceback, if an exception occurred.
        """
        await self.aclose()
