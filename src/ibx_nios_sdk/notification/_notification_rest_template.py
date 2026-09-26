# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRestTemplateResource - NIOS notification REST template, GET+PUT+DELETE only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.notification.models.notification_rest_template import (
    READONLY_FIELDS,
    NotificationRestTemplate,
)


class NotificationRestTemplateResource(WapiResource[NotificationRestTemplate]):
    """Manage NIOS notification REST template objects."""

    _wapi_type = "notification:rest:template"
    _model = NotificationRestTemplate
    _default_return_fields = ["name", "outbound_type"]
    _readonly_fields = set(READONLY_FIELDS)
