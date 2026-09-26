# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CsvimporttaskResource - NIOS CSV import task, GET+PUT only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.csvimporttask import READONLY_FIELDS, Csvimporttask


class CsvimporttaskResource(WapiResource[Csvimporttask]):
    """Access NIOS CSV import task records (read-only)."""

    _wapi_type = "csvimporttask"
    _model = Csvimporttask
    _default_return_fields = ["file_name", "status", "action", "operation"]
    _readonly_fields = set(READONLY_FIELDS)
