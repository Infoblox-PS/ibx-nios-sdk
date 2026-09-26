# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DatacollectionclusterResource - NIOS data collection cluster, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.datacollectioncluster import (
    READONLY_FIELDS,
    Datacollectioncluster,
)


class DatacollectionclusterResource(WapiResource[Datacollectioncluster]):
    """Manage NIOS data collection cluster objects."""

    _wapi_type = "datacollectioncluster"
    _model = Datacollectioncluster
    _default_return_fields = ["name", "enable_registration"]
    _readonly_fields = set(READONLY_FIELDS)
