# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Live: list every object type with its full readable field set from ``?_schema``.

Run with ``NIOS_LIVE=1 pytest tests/integration/test_full_return_fields_live.py``.
Uses the same lab grid constants as ``test_smoke_live``. Object types that need a
mandatory search argument (``zone``, ``network``, ``dtc_server``...) or are not
readable are skipped when NIOS says so.
"""

from __future__ import annotations

import os

import pytest

if not os.getenv("NIOS_LIVE"):
    pytest.skip("set NIOS_LIVE=1 to run live tests", allow_module_level=True)

from ibx_nios_sdk import NiosClient  # noqa: E402
from ibx_nios_sdk._exceptions import BadRequestError, NiosError  # noqa: E402
from ibx_nios_sdk._restrictions import restricted_ops  # noqa: E402
from tests.integration.test_smoke_live import (  # noqa: E402
    GRID_URL,
    PASSWORD,
    USERNAME,
    VERIFY,
    WAPI_VERSION,
)
from tests.wapi_schema import ResourceInfo, iter_resources  # noqa: E402

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

UNLISTABLE_MARKERS = (
    "Required search parameter",
    "search parameters is required",
    "Search fields must contain",
    "must be specified",
    "Operation read not allowed",
    "is required for retrieving",
    "No response from discovery service",
    "Failed to get the response from cloud service",
    "Site not found",
    "Unknown object type",
)


@pytest.fixture(scope="module")
async def client():
    async with NiosClient(
        grid_url=GRID_URL,
        username=USERNAME,
        password=PASSWORD,
        verify=VERIFY,
        wapi_version=WAPI_VERSION,
    ) as c:
        yield c


# Six object types (dtc, discovery, fedipamop, ...) restrict read: NIOS answers
# "Operation read not allowed" and the SDK refuses the call locally. There is no
# row to fetch, so they are not part of this suite.
LISTABLE = [r for r in iter_resources() if "read" not in restricted_ops(r.wapi_type)]


@pytest.mark.parametrize("res", LISTABLE, ids=lambda r: r.wapi_type)
async def test_list_full_readable_fields_live(client: NiosClient, res: ResourceInfo) -> None:
    try:
        raw = await client._http.get(
            res.wapi_type, params={"_schema": "1", "_schema_version": "2"}
        )
    except BadRequestError as exc:
        pytest.skip(f"{res.wapi_type}: {exc}")
    schema_obj = raw["_value"] if isinstance(raw, dict) and "_value" in raw else raw
    fields = [
        f["name"]
        for f in schema_obj["fields"]
        if "r" in f["supports"] and f.get("wapi_primitive") != "funccall"
    ]
    resource = res.resource(client._http)
    try:
        rows, _ = await resource.list_page(max_results=5, return_fields=fields)
    except NiosError as exc:
        if any(marker in str(exc) for marker in UNLISTABLE_MARKERS):
            pytest.skip(f"{res.wapi_type} needs a search argument: {exc}")
        raise
    if not rows:
        pytest.skip(f"no {res.wapi_type} objects on the lab grid")
