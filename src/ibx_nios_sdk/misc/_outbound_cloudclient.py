# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""OutboundCloudclientResource - NIOS outbound cloud client, GET+PUT only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.outbound_cloudclient import READONLY_FIELDS, OutboundCloudclient


class OutboundCloudclientResource(WapiResource[OutboundCloudclient]):
    """Manage NIOS outbound cloud client objects."""

    _wapi_type = "outbound:cloudclient"
    _model = OutboundCloudclient
    _default_return_fields = ["grid_member", "enable", "interval"]
    _readonly_fields = set(READONLY_FIELDS)
