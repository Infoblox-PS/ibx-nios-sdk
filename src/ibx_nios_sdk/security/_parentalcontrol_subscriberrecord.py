# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscriberrecord resource - NIOS parental-control subscriber record."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.parentalcontrol_subscriberrecord import (
    READONLY_FIELDS,
    ParentalcontrolSubscriberrecord,
)


class ParentalcontrolSubscriberrecordResource(WapiResource[ParentalcontrolSubscriberrecord]):
    """Manage NIOS parental-control subscriber records."""

    _wapi_type = "parentalcontrol:subscriberrecord"
    _model = ParentalcontrolSubscriberrecord
    _default_return_fields = ["subscriber_id", "ip_addr", "site", "parental_control_policy"]
    _readonly_fields = set(READONLY_FIELDS)
