# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverAdsitesSiteResource - NIOS MS server AD sites site, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.microsoftserver.models.msserver_adsites_site import (
    READONLY_FIELDS,
    MsserverAdsitesSite,
)


class MsserverAdsitesSiteResource(WapiResource[MsserverAdsitesSite]):
    """Manage NIOS Microsoft server AD sites site objects."""

    _wapi_type = "msserver:adsites:site"
    _model = MsserverAdsitesSite
    _default_return_fields = ["name", "domain"]
    _readonly_fields = set(READONLY_FIELDS)
