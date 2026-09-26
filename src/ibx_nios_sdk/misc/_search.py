# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Search - WAPI global search endpoint (function-only)."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._http import HttpClient, unwrap_value


class SearchResource:
    """Function-only resource at /search.

    WAPI global search is invoked via GET /search with query parameters.
    Function calls use POST /search?_function=<name>.
    """

    def __init__(self, client: HttpClient) -> None:
        """Initialise SearchResource with an authenticated HTTP client."""
        self._client = client

    async def search(self, **kwargs: Any) -> list[dict[str, Any]]:
        """Perform a global search across NIOS objects via GET /search.

        Keyword arguments are converted to query parameters and passed to the
        WAPI ``/search`` endpoint. The SDK HTTP layer wraps JSON array responses
        as ``{"_value": [...]}``, which this method unwraps transparently.

        Args:
            **kwargs: WAPI search query parameters. Common fields include:
                - ``search_string``: The text to search for across object attributes.
                - ``objtype``: Limit results to a specific WAPI object type.
                - ``_max_results``: Maximum number of results to return.

        Returns:
            A list of dicts, where each dict represents a matching WAPI object.
            Returns an empty list if no results are found or the response is empty.

        Raises:
            WapiRequestError: If the WAPI search call fails.
        """
        params = {k: str(v) for k, v in kwargs.items() if v is not None}
        data = await self._client.get("/search", params=params or None)
        value = unwrap_value(data)
        return list(value) if isinstance(value, list) else []

    async def call(self, function: str, **kwargs: Any) -> dict[str, Any]:
        """Dispatch a WAPI search function call via POST /search?_function=<function>.

        Args:
            function: The WAPI search function name.
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
        data = await self._client.post("/search", params=params, json=body or None)
        return data or {}
