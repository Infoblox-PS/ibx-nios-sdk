# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AzurednstaskgroupResource - NIOS Azure DNS task group, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.cloud.models.azurednstaskgroup import READONLY_FIELDS, Azurednstaskgroup


class AzurednstaskgroupResource(WapiResource[Azurednstaskgroup]):
    """Manage NIOS Azure DNS task group objects."""

    _wapi_type = "azurednstaskgroup"
    _model = Azurednstaskgroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {
        "consolidate_zones",
        "consolidated_view",
        "multiple_subscriptions_sync_policy",
        "network_view",
        "network_view_mapping_policy",
    }
