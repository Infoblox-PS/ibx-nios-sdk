# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ApprovalworkflowResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.approvalworkflow import READONLY_FIELDS, Approvalworkflow


class ApprovalworkflowResource(WapiResource[Approvalworkflow]):
    """Manage NIOS approval workflow objects."""

    _wapi_type = "approvalworkflow"
    _model = Approvalworkflow
    _default_return_fields = ["approval_group", "submitter_group", "ticket_number"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"submitter_group"}
