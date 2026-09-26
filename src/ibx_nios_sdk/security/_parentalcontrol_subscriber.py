# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscriber resource - NIOS parental-control subscriber configuration."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.parentalcontrol_subscriber import (
    READONLY_FIELDS,
    ParentalcontrolSubscriber,
)


class ParentalcontrolSubscriberResource(WapiResource[ParentalcontrolSubscriber]):
    """Manage NIOS parental-control subscriber configuration."""

    _wapi_type = "parentalcontrol:subscriber"
    _model = ParentalcontrolSubscriber
    _default_return_fields = [
        "subscriber_id",
        "enable_parental_control",
        "pc_zone_name",
        "category_url",
    ]
    _readonly_fields = set(READONLY_FIELDS)
