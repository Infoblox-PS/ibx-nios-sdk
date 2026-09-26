# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GcpuserResource - NIOS GCP user, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.cloud.models.gcpuser import READONLY_FIELDS, Gcpuser


class GcpuserResource(WapiResource[Gcpuser]):
    """Manage NIOS GCP user credentials objects."""

    _wapi_type = "gcpuser"
    _model = Gcpuser
    _default_return_fields = ["user_name"]
    _readonly_fields = set(READONLY_FIELDS)
