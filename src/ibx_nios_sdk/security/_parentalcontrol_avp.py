# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolAvp resource - NIOS parental-control AVP."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.parentalcontrol_avp import (
    READONLY_FIELDS,
    ParentalcontrolAvp,
)


class ParentalcontrolAvpResource(WapiResource[ParentalcontrolAvp]):
    """Manage NIOS parental-control AVP definitions."""

    _wapi_type = "parentalcontrol:avp"
    _model = ParentalcontrolAvp
    _default_return_fields = ["name", "type", "value_type", "vendor_id", "vendor_type", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
