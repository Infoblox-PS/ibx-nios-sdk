# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DeletedObjectsResource - NIOS deleted objects, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.deleted_objects import READONLY_FIELDS, DeletedObjects


class DeletedObjectsResource(WapiResource[DeletedObjects]):
    """Access NIOS deleted object records (read-only aggregate)."""

    _wapi_type = "deleted_objects"
    _model = DeletedObjects
    _default_return_fields = ["object_type"]
    _readonly_fields = set(READONLY_FIELDS)
