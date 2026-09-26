# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""TaxiiResource - NIOS TAXII, GET+PUT only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.taxii import READONLY_FIELDS, Taxii


class TaxiiResource(WapiResource[Taxii]):
    """Manage NIOS TAXII configuration objects."""

    _wapi_type = "taxii"
    _model = Taxii
    _default_return_fields = ["name", "enable_service", "ipv4addr"]
    _readonly_fields = set(READONLY_FIELDS)
