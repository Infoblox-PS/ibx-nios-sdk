# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordAaaaResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_record_aaaa import READONLY_FIELDS, DtcRecordAaaa


class DtcRecordAaaaResource(WapiResource[DtcRecordAaaa]):
    """Manage NIOS DTC AAAA record objects."""

    _wapi_type = "dtc:record:aaaa"
    _model = DtcRecordAaaa
    _default_return_fields = ["ipv6addr", "dtc_server", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"dtc_server"}
