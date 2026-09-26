# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MultiregionsResource - NIOS multi-regions, GET+PUT only (no POST, no DELETE)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.cloud.models.multiregions import READONLY_FIELDS, Multiregions


class MultiregionsResource(WapiResource[Multiregions]):
    """Manage NIOS cloud multi-region objects."""

    _wapi_type = "multiregions"
    _model = Multiregions
    _default_return_fields = ["cloud_platform"]
    _readonly_fields = set(READONLY_FIELDS)
