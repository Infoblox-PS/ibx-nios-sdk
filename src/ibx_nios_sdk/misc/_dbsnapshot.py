# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DbsnapshotResource - NIOS database snapshot, GET+PUT only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.dbsnapshot import READONLY_FIELDS, Dbsnapshot


class DbsnapshotResource(WapiResource[Dbsnapshot]):
    """Manage NIOS database snapshot objects."""

    _wapi_type = "dbsnapshot"
    _model = Dbsnapshot
    _default_return_fields = ["comment", "timestamp"]
    _readonly_fields = set(READONLY_FIELDS)
