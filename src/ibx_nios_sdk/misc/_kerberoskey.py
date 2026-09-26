# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""KerberoskeyResource - NIOS Kerberos key, GET+DELETE only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.kerberoskey import READONLY_FIELDS, Kerberoskey


class KerberoskeyResource(WapiResource[Kerberoskey]):
    """Manage NIOS Kerberos key objects."""

    _wapi_type = "kerberoskey"
    _model = Kerberoskey
    _default_return_fields = ["principal", "domain", "enctype", "version"]
    _readonly_fields = set(READONLY_FIELDS)
