# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DNS-specific test helpers."""

from __future__ import annotations

import httpx

from tests.conftest import json_response


def dns_session_handler_factory(path_response_map):
    """Build a MockTransport handler that logs in, then routes by path to the
    (status, body) pair provided in ``path_response_map``.

    path_response_map: dict[str, tuple[int, Any]] - path -> (status_code, body)
    """
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls.append(request)
        for path, (status, body) in path_response_map.items():
            if path in request.url.path:
                return json_response(body, status_code=status)
        return json_response({"Error": "no handler", "text": request.url.path}, status_code=404)

    return handler, calls
