# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Fileop - WAPI fileop endpoint (function-only, not CRUD)."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._http import HttpClient


class FileopResource:
    """Function-only resource at /fileop.

    All WAPI fileop functions are invoked via POST /fileop?_function=<name>.
    """

    def __init__(self, client: HttpClient) -> None:
        """Initialise FileopResource with an authenticated HTTP client."""
        self._client = client

    async def call(self, function: str, **kwargs: Any) -> dict[str, Any]:
        """Dispatch a WAPI fileop function call via POST /fileop?_function=<function>.

        Args:
            function: The WAPI fileop function name (e.g. ``"uploadinit"``).
            **kwargs: Additional keyword arguments sent as JSON body fields.
                Fields with ``None`` values are omitted from the request body.

        Returns:
            A dict containing the WAPI function response, or an empty dict
            if the response body is empty.

        Raises:
            WapiRequestError: If the WAPI call fails or returns an error status.
        """
        params = {"_function": function}
        body = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._client.post("/fileop", params=params, json=body or None)
        return data or {}

    async def upload_init(self, **kwargs: Any) -> dict[str, Any]:
        """Initiate a file upload session, returning an upload token and URL.

        Calls the WAPI ``uploadinit`` fileop function. The returned token must be
        passed to subsequent upload requests.

        Args:
            **kwargs: WAPI ``uploadinit`` parameters passed as JSON body fields.
                Common fields include ``type`` (e.g. ``"CSV"``) and ``filename``.

        Returns:
            A dict containing ``token`` (upload session token) and ``url``
            (the upload destination URL).

        Raises:
            WapiRequestError: If the WAPI call fails or the session cannot be initiated.
        """
        return await self.call("uploadinit", **kwargs)

    async def upload_certificate(self, **kwargs: Any) -> dict[str, Any]:
        """Upload a certificate file after calling upload_init.

        Calls the WAPI ``uploadcertificate`` fileop function.

        Args:
            **kwargs: WAPI ``uploadcertificate`` parameters. Typically includes
                ``token`` (from a prior ``upload_init`` call) and ``certificate``
                content fields.

        Returns:
            A dict containing the WAPI function response, typically empty on success.

        Raises:
            WapiRequestError: If the WAPI call fails or the certificate is invalid.
        """
        return await self.call("uploadcertificate", **kwargs)

    async def csv_import(self, **kwargs: Any) -> dict[str, Any]:
        """Import CSV data into NIOS via the WAPI fileop endpoint.

        Calls the WAPI ``csv_import`` fileop function.

        Args:
            **kwargs: WAPI ``csv_import`` parameters. Common fields include
                ``token`` (from ``upload_init``), ``action`` (e.g. ``"START"``),
                and ``on_error`` (e.g. ``"STOP"``).

        Returns:
            A dict containing the WAPI function response, including import task
            details such as ``import_id`` and status information.

        Raises:
            WapiRequestError: If the WAPI call fails or the CSV is malformed.
        """
        return await self.call("csv_import", **kwargs)

    async def csv_export(self, **kwargs: Any) -> dict[str, Any]:
        """Export NIOS object data as a CSV file via the WAPI fileop endpoint.

        Calls the WAPI ``csv_export`` fileop function.

        Args:
            **kwargs: WAPI ``csv_export`` parameters. Common fields include
                ``_object`` (the WAPI object type to export, e.g. ``"network"``)
                and any applicable search filters.

        Returns:
            A dict containing the WAPI function response, typically including
            a ``token`` that can be used to retrieve the exported file.

        Raises:
            WapiRequestError: If the WAPI call fails or the export cannot be started.
        """
        return await self.call("csv_export", **kwargs)

    async def csv_snapshot_file(self, **kwargs: Any) -> dict[str, Any]:
        """Retrieve a previously generated CSV snapshot file.

        Calls the WAPI ``csv_snapshot_file`` fileop function.

        Args:
            **kwargs: WAPI ``csv_snapshot_file`` parameters. Typically includes
                ``token`` identifying the snapshot file to retrieve.

        Returns:
            A dict containing the WAPI function response with snapshot file details.

        Raises:
            WapiRequestError: If the WAPI call fails or the snapshot token is invalid.
        """
        return await self.call("csv_snapshot_file", **kwargs)

    async def download_complete(self, **kwargs: Any) -> dict[str, Any]:
        """Signal to NIOS that a file download has completed successfully.

        Calls the WAPI ``downloadcomplete`` fileop function. This should be called
        after fully reading a file obtained from a prior download operation.

        Args:
            **kwargs: WAPI ``downloadcomplete`` parameters. Typically includes
                ``token`` identifying the completed download session.

        Returns:
            A dict containing the WAPI function response, typically empty on success.

        Raises:
            WapiRequestError: If the WAPI call fails or the token is invalid.
        """
        return await self.call("downloadcomplete", **kwargs)

    async def downloadcertificate(self, **kwargs: Any) -> dict[str, Any]:
        """Download a certificate from NIOS via the WAPI fileop endpoint.

        Calls the WAPI ``downloadcertificate`` fileop function.

        Args:
            **kwargs: WAPI ``downloadcertificate`` parameters. Common fields include
                ``certificate_usage`` (e.g. ``"HTTP_CERT"``).

        Returns:
            A dict containing the WAPI function response, typically including
            a ``token`` for retrieving the certificate content.

        Raises:
            WapiRequestError: If the WAPI call fails or the certificate is unavailable.
        """
        return await self.call("downloadcertificate", **kwargs)
