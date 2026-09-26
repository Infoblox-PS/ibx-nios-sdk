# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FederatedrealmsResource - NIOS federated realm, GET only (no write ops)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.federatedrealms.models.federatedrealms import (
    READONLY_FIELDS,
    Federatedrealms,
)


class FederatedrealmsResource(WapiResource[Federatedrealms]):
    """Manage NIOS federated realms configuration objects."""

    _wapi_type = "federatedrealms"
    _model = Federatedrealms
    _default_return_fields = ["id", "name"]
    _readonly_fields = set(READONLY_FIELDS)
