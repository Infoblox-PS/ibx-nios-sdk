# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRestEndpointResource - NIOS notification REST endpoint, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.notification.models.notification_rest_endpoint import (
    READONLY_FIELDS,
    NotificationRestEndpoint,
)


class NotificationRestEndpointResource(WapiResource[NotificationRestEndpoint]):
    """Manage NIOS notification REST endpoint objects."""

    _wapi_type = "notification:rest:endpoint"
    _model = NotificationRestEndpoint
    _default_return_fields = ["name", "uri", "log_level"]
    _readonly_fields = set(READONLY_FIELDS)
