# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""BfdtemplateResource - NIOS BFD template, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.bfdtemplate import READONLY_FIELDS, Bfdtemplate


class BfdtemplateResource(WapiResource[Bfdtemplate]):
    """Manage NIOS BFD template objects."""

    _wapi_type = "bfdtemplate"
    _model = Bfdtemplate
    _default_return_fields = ["name", "detection_multiplier", "min_rx_interval", "min_tx_interval"]
    _readonly_fields = set(READONLY_FIELDS)
