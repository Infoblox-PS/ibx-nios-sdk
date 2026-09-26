# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CacertificateResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.cacertificate import READONLY_FIELDS, Cacertificate


class CacertificateResource(WapiResource[Cacertificate]):
    """Access NIOS CA certificate objects (read-only aggregate)."""

    _wapi_type = "cacertificate"
    _model = Cacertificate
    _default_return_fields = ["distinguished_name", "issuer", "serial"]
    _readonly_fields = set(READONLY_FIELDS)
