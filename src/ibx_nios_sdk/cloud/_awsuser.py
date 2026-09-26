# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AwsuserResource - NIOS AWS user, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.cloud.models.awsuser import READONLY_FIELDS, Awsuser


class AwsuserResource(WapiResource[Awsuser]):
    """Manage NIOS AWS user credentials objects."""

    _wapi_type = "awsuser"
    _model = Awsuser
    _default_return_fields = ["name"]
    _readonly_fields = set(READONLY_FIELDS)
