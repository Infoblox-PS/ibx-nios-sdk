# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberParentalcontrolResource - NIOS member parental control service."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member_parentalcontrol import (
    READONLY_FIELDS,
    MemberParentalcontrol,
)


class MemberParentalcontrolResource(WapiResource[MemberParentalcontrol]):
    """Manage NIOS member parental control configurations."""

    _wapi_type = "member:parentalcontrol"
    _model = MemberParentalcontrol
    _default_return_fields = ["name", "enable_service"]
    _readonly_fields = set(READONLY_FIELDS)
