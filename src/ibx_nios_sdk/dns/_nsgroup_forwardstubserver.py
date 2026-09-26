# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupForwardstubserver resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.nsgroup_forwardstubserver import (
    READONLY_FIELDS,
    NsgroupForwardstubserver,
)


class NsgroupForwardstubserverResource(WapiResource[NsgroupForwardstubserver]):
    """Manage NIOS DNS forwarding and stub server name-server groups."""

    _wapi_type = "nsgroup:forwardstubserver"
    _model = NsgroupForwardstubserver
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
