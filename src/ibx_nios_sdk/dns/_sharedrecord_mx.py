# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordMx resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.sharedrecord_mx import READONLY_FIELDS, SharedrecordMx


class SharedrecordMxResource(WapiResource[SharedrecordMx]):
    """Manage NIOS shared DNS MX records (mail exchangers shared across zones)."""

    _wapi_type = "sharedrecord:mx"
    _model = SharedrecordMx
    _default_return_fields = [
        "name",
        "mail_exchanger",
        "preference",
        "shared_record_group",
        "comment",
    ]
    _readonly_fields = set(READONLY_FIELDS)
