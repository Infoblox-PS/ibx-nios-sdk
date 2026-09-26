# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ScavengingtaskResource - NIOS scavenging task, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.scavengingtask import READONLY_FIELDS, Scavengingtask


class ScavengingtaskResource(WapiResource[Scavengingtask]):
    """Manage NIOS DNS scavenging task objects."""

    _wapi_type = "scavengingtask"
    _model = Scavengingtask
    _default_return_fields = ["status", "action", "start_time", "end_time"]
    _readonly_fields = set(READONLY_FIELDS)
