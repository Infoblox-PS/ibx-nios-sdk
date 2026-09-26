# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordCname resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.sharedrecord_cname import READONLY_FIELDS, SharedrecordCname


class SharedrecordCnameResource(WapiResource[SharedrecordCname]):
    """Manage NIOS shared DNS CNAME records (aliases shared across zones)."""

    _wapi_type = "sharedrecord:cname"
    _model = SharedrecordCname
    _default_return_fields = ["name", "canonical", "shared_record_group", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
