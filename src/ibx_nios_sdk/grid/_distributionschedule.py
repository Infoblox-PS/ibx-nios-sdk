# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DistributionscheduleResource - NIOS distribution schedule."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.distributionschedule import READONLY_FIELDS, Distributionschedule


class DistributionscheduleResource(WapiResource[Distributionschedule]):
    """Manage NIOS software distribution schedule objects."""

    _wapi_type = "distributionschedule"
    _model = Distributionschedule
    _default_return_fields = ["active", "start_time"]
    _readonly_fields = set(READONLY_FIELDS)
