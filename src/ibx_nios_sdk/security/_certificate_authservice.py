# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CertificateAuthserviceResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.certificate_authservice import (
    READONLY_FIELDS,
    CertificateAuthservice,
)


class CertificateAuthserviceResource(WapiResource[CertificateAuthservice]):
    """Manage NIOS certificate-based authentication service objects."""

    _wapi_type = "certificate:authservice"
    _model = CertificateAuthservice
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
