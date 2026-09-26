# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupDelegation resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.nsgroup_delegation import READONLY_FIELDS, NsgroupDelegation


class NsgroupDelegationResource(WapiResource[NsgroupDelegation]):
    """Manage NIOS DNS name-server groups for delegation zones."""

    _wapi_type = "nsgroup:delegation"
    _model = NsgroupDelegation
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
