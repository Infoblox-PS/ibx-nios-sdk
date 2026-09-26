# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupStubmember resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.nsgroup_stubmember import READONLY_FIELDS, NsgroupStubmember


class NsgroupStubmemberResource(WapiResource[NsgroupStubmember]):
    """Manage NIOS DNS name-server groups for stub zone members."""

    _wapi_type = "nsgroup:stubmember"
    _model = NsgroupStubmember
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
