# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Request - WAPI generic multi-request endpoint (POST-only, body-only)."""

from __future__ import annotations

from typing import Any, cast

from ibx_nios_sdk._http import HttpClient, unwrap_value


class RequestResource:
    """Function-only resource at /request.

    The WAPI ``/request`` endpoint accepts a POST body containing one or more
    requests to execute in sequence (optionally as a transaction). Only POST is
    supported - the NIOS WAPI rejects GET on this endpoint.
    """

    def __init__(self, client: HttpClient) -> None:
        """Initialise RequestResource with an authenticated HTTP client."""
        self._client = client

    async def submit(
        self, body: list[dict[str, Any]] | dict[str, Any]
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """POST a batched or single request body to ``/request``.

        Args:
            body: Either a list of individual request dicts, or a single dict.
                Each request dict typically contains ``method``, ``object``,
                ``data``, and optional ``args`` / ``assign_state`` fields.

        Returns:
            The WAPI response. For batched calls this is a list of per-request
            results in the same order as the input.

        Raises:
            WapiRequestError: If the WAPI call fails.
        """
        # /request accepts a list body despite HttpClient.post being dict-typed;
        # cast here rather than leaking the Union through the HTTP layer.
        data = await self._client.post("/request", json=cast("dict[str, Any]", body))
        unwrapped = unwrap_value(data)
        if unwrapped is None:
            return []
        return cast("list[dict[str, Any]] | dict[str, Any]", unwrapped)
