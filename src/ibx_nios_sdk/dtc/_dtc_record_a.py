# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordAResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_record_a import READONLY_FIELDS, DtcRecordA


class DtcRecordAResource(WapiResource[DtcRecordA]):
    """Manage NIOS DTC A record objects."""

    _wapi_type = "dtc:record:a"
    _model = DtcRecordA
    _default_return_fields = ["ipv4addr", "dtc_server", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"dtc_server"}
