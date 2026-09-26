# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordCnameResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_record_cname import READONLY_FIELDS, DtcRecordCname


class DtcRecordCnameResource(WapiResource[DtcRecordCname]):
    """Manage NIOS DTC CNAME record objects."""

    _wapi_type = "dtc:record:cname"
    _model = DtcRecordCname
    _default_return_fields = ["canonical", "dtc_server", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"dtc_server"}
