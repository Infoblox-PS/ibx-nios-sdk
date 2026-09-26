# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRuleResource - NIOS notification rule, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.notification.models.notification_rule import (
    READONLY_FIELDS,
    NotificationRule,
)


class NotificationRuleResource(WapiResource[NotificationRule]):
    """Manage NIOS notification rule objects."""

    _wapi_type = "notification:rule"
    _model = NotificationRule
    _default_return_fields = ["name", "event_type", "notification_action"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"name"}
