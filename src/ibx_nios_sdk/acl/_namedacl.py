# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NamedaclResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.acl.models.namedacl import READONLY_FIELDS, Namedacl


class NamedaclResource(WapiResource[Namedacl]):
    """Manage NIOS named ACL (Access Control List) objects."""

    _wapi_type = "namedacl"
    _model = Namedacl
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
