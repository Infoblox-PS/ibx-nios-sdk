# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmAllgroupsResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.hsm_allgroups import READONLY_FIELDS, HsmAllgroups


class HsmAllgroupsResource(WapiResource[HsmAllgroups]):
    """Access NIOS HSM all-groups aggregate (read-only)."""

    _wapi_type = "hsm:allgroups"
    _model = HsmAllgroups
    _default_return_fields = ["groups"]
    _readonly_fields = set(READONLY_FIELDS)
