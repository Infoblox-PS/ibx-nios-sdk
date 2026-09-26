# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MembercloudsyncResource - NIOS member cloud sync settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.membercloudsync import READONLY_FIELDS, Membercloudsync


class MembercloudsyncResource(WapiResource[Membercloudsync]):
    """Manage NIOS member cloud sync configurations."""

    _wapi_type = "membercloudsync"
    _model = Membercloudsync
    _default_return_fields = ["host_name", "cloud_sync_enabled"]
    _readonly_fields = set(READONLY_FIELDS)
