# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscribersite resource - NIOS parental-control subscriber site."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.parentalcontrol_subscribersite import (
    READONLY_FIELDS,
    ParentalcontrolSubscribersite,
)


class ParentalcontrolSubscribersiteResource(WapiResource[ParentalcontrolSubscribersite]):
    """Manage NIOS parental-control subscriber sites."""

    _wapi_type = "parentalcontrol:subscribersite"
    _model = ParentalcontrolSubscribersite
    _default_return_fields = [
        "name",
        "blocking_ipv4_vip1",
        "blocking_ipv4_vip2",
        "maximum_subscribers",
        "comment",
    ]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"name"}
