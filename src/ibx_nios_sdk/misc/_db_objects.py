# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DbObjectsResource - NIOS database objects, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.db_objects import READONLY_FIELDS, DbObjects


class DbObjectsResource(WapiResource[DbObjects]):
    """Access NIOS database object records (read-only aggregate)."""

    _wapi_type = "db_objects"
    _model = DbObjects
    _default_return_fields = ["object_type", "object", "unique_id"]
    _readonly_fields = set(READONLY_FIELDS)
