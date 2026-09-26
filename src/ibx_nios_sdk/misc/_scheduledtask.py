# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ScheduledtaskResource - NIOS scheduled task, GET+PUT+DELETE."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.scheduledtask import READONLY_FIELDS, Scheduledtask


class ScheduledtaskResource(WapiResource[Scheduledtask]):
    """Access NIOS scheduled task records (read-only)."""

    _wapi_type = "scheduledtask"
    _model = Scheduledtask
    _default_return_fields = [
        "task_id",
        "task_type",
        "scheduled_time",
        "execution_status",
        "approval_status",
    ]
    _readonly_fields = set(READONLY_FIELDS)
