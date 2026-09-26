# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Awsrte53taskgroupResource - NIOS AWS Route53 task group, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.cloud.models.awsrte53taskgroup import READONLY_FIELDS, Awsrte53taskgroup


class Awsrte53taskgroupResource(WapiResource[Awsrte53taskgroup]):
    """Manage NIOS AWS Route 53 task group objects."""

    _wapi_type = "awsrte53taskgroup"
    _model = Awsrte53taskgroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {
        "consolidate_zones",
        "consolidated_view",
        "network_view",
        "network_view_mapping_policy",
    }
