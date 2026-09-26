# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordNaptrResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_record_naptr import READONLY_FIELDS, DtcRecordNaptr


class DtcRecordNaptrResource(WapiResource[DtcRecordNaptr]):
    """Manage NIOS DTC NAPTR record objects."""

    _wapi_type = "dtc:record:naptr"
    _model = DtcRecordNaptr
    _default_return_fields = ["services", "dtc_server", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"dtc_server"}
