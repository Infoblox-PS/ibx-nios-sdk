# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""TacacsplusAuthserviceResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.tacacsplus_authservice import (
    READONLY_FIELDS,
    TacacsplusAuthservice,
)


class TacacsplusAuthserviceResource(WapiResource[TacacsplusAuthservice]):
    """Manage NIOS TACACS+ authentication service objects."""

    _wapi_type = "tacacsplus:authservice"
    _model = TacacsplusAuthservice
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
