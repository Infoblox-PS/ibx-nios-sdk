# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcLbdnResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_lbdn import READONLY_FIELDS, DtcLbdn


class DtcLbdnResource(WapiResource[DtcLbdn]):
    """Manage NIOS DTC load-balanced domain name (LBDN) objects."""

    _wapi_type = "dtc:lbdn"
    _model = DtcLbdn
    _default_return_fields = ["name", "comment", "lb_method"]
    _readonly_fields = set(READONLY_FIELDS)
