# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolBlockingpolicy resource - NIOS parental-control blocking policy."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.parentalcontrol_blockingpolicy import (
    READONLY_FIELDS,
    ParentalcontrolBlockingpolicy,
)


class ParentalcontrolBlockingpolicyResource(WapiResource[ParentalcontrolBlockingpolicy]):
    """Manage NIOS parental-control blocking policies."""

    _wapi_type = "parentalcontrol:blockingpolicy"
    _model = ParentalcontrolBlockingpolicy
    _default_return_fields = ["name", "value"]
    _readonly_fields = set(READONLY_FIELDS)
