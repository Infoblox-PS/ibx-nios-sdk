# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberFiledistributionResource - NIOS member file distribution settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member_filedistribution import (
    READONLY_FIELDS,
    MemberFiledistribution,
)


class MemberFiledistributionResource(WapiResource[MemberFiledistribution]):
    """Manage NIOS member file distribution configurations."""

    _wapi_type = "member:filedistribution"
    _model = MemberFiledistribution
    _default_return_fields = ["host_name", "comment", "status"]
    _readonly_fields = set(READONLY_FIELDS)
