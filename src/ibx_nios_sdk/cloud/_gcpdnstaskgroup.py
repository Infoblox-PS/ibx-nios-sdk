# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GcpdnstaskgroupResource - NIOS GCP DNS task group, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.cloud.models.gcpdnstaskgroup import READONLY_FIELDS, Gcpdnstaskgroup


class GcpdnstaskgroupResource(WapiResource[Gcpdnstaskgroup]):
    """Manage NIOS GCP DNS task group objects."""

    _wapi_type = "gcpdnstaskgroup"
    _model = Gcpdnstaskgroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {
        "consolidate_zones",
        "consolidated_view",
        "network_view",
        "network_view_mapping_policy",
    }
