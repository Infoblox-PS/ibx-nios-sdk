# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcCertificateResource - GET only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_certificate import READONLY_FIELDS, DtcCertificate


class DtcCertificateResource(WapiResource[DtcCertificate]):
    """Manage NIOS DTC certificate objects."""

    _wapi_type = "dtc:certificate"
    _model = DtcCertificate
    _default_return_fields = ["uuid", "in_use"]
    _readonly_fields = set(READONLY_FIELDS)
