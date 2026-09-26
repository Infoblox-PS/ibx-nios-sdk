# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Nsgroup resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.nsgroup import READONLY_FIELDS, Nsgroup


class NsgroupResource(WapiResource[Nsgroup]):
    """Manage NIOS DNS name-server group configurations."""

    _wapi_type = "nsgroup"
    _model = Nsgroup
    _default_return_fields = ["name", "comment", "is_grid_default"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"is_multimaster"}
