# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FedipamopResource - NIOS federated IPAM operation, GET+PUT only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.federatedrealms.models.fedipamop import READONLY_FIELDS, Fedipamop


class FedipamopResource(WapiResource[Fedipamop]):
    """Manage NIOS federated IPAM operation objects."""

    _wapi_type = "fedipamop"
    _model = Fedipamop
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
