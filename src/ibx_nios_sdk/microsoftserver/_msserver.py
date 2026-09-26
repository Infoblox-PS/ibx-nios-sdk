# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverResource - NIOS Microsoft server, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.microsoftserver.models.msserver import READONLY_FIELDS, Msserver


class MsserverResource(WapiResource[Msserver]):
    """Manage NIOS Microsoft server objects."""

    _wapi_type = "msserver"
    _model = Msserver
    _default_return_fields = ["address", "server_name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
