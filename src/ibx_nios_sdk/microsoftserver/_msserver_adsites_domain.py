# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverAdsitesDomainResource - NIOS MS server AD sites domain, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.microsoftserver.models.msserver_adsites_domain import (
    READONLY_FIELDS,
    MsserverAdsitesDomain,
)


class MsserverAdsitesDomainResource(WapiResource[MsserverAdsitesDomain]):
    """Manage NIOS Microsoft server AD sites domain objects."""

    _wapi_type = "msserver:adsites:domain"
    _model = MsserverAdsitesDomain
    _default_return_fields = ["name", "netbios", "network_view"]
    _readonly_fields = set(READONLY_FIELDS)
