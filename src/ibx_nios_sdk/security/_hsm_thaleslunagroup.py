# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmThaleslunagroupResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.hsm_thaleslunagroup import (
    READONLY_FIELDS,
    HsmThaleslunagroup,
)


class HsmThaleslunagroupResource(WapiResource[HsmThaleslunagroup]):
    """Manage NIOS HSM Thales Luna group objects."""

    _wapi_type = "hsm:thaleslunagroup"
    _model = HsmThaleslunagroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"hsm_version"}
