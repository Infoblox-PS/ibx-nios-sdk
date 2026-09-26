# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Rir resource - NIOS Regional Internet Registry."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.rir import READONLY_FIELDS, Rir


class RirResource(WapiResource[Rir]):
    """Manage NIOS Regional Internet Registry (RIR) configuration."""

    _wapi_type = "rir"
    _model = Rir
    _default_return_fields = ["name", "communication_mode", "email", "url"]
    _readonly_fields = set(READONLY_FIELDS)
