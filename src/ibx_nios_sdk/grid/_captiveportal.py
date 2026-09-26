# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CaptiveportalResource - NIOS captive portal settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.captiveportal import READONLY_FIELDS, Captiveportal


class CaptiveportalResource(WapiResource[Captiveportal]):
    """Manage NIOS captive portal configurations."""

    _wapi_type = "captiveportal"
    _model = Captiveportal
    _default_return_fields = ["name", "company_name", "service_enabled"]
    _readonly_fields = set(READONLY_FIELDS)
