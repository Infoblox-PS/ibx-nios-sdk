# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RirOrganization resource - NIOS RIR organization."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.rir_organization import READONLY_FIELDS, RirOrganization


class RirOrganizationResource(WapiResource[RirOrganization]):
    """Manage NIOS RIR organizations."""

    _wapi_type = "rir:organization"
    _model = RirOrganization
    _default_return_fields = ["name", "id", "rir", "maintainer", "sender_email"]
    _readonly_fields = set(READONLY_FIELDS)
