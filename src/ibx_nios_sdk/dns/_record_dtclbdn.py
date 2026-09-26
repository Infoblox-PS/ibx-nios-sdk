# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDtclbdn resource - read-only DTC LBDN DNS record projection."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_dtclbdn import READONLY_FIELDS, RecordDtclbdn


class RecordDtclbdnResource(WapiResource[RecordDtclbdn]):
    """Manage (read) NIOS DTC LBDN DNS records."""

    _wapi_type = "record:dtclbdn"
    _model = RecordDtclbdn
    _default_return_fields = ["name", "view", "zone", "pattern", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
