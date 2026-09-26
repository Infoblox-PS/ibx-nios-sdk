# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryCredentialgroupResource - NIOS discovery credential group, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_credentialgroup import (
    READONLY_FIELDS,
    DiscoveryCredentialgroup,
)


class DiscoveryCredentialgroupResource(WapiResource[DiscoveryCredentialgroup]):
    """Manage NIOS network discovery credential group objects."""

    _wapi_type = "discovery:credentialgroup"
    _model = DiscoveryCredentialgroup
    _default_return_fields = ["name", "uuid"]
    _readonly_fields = set(READONLY_FIELDS)
