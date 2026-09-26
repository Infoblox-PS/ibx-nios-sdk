# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationService - entry point for notification resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.notification._notification_rest_endpoint import (
        NotificationRestEndpointResource,
    )
    from ibx_nios_sdk.notification._notification_rest_template import (
        NotificationRestTemplateResource,
    )
    from ibx_nios_sdk.notification._notification_rule import NotificationRuleResource


class NotificationService:
    """Entry point for NIOS notification resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise NotificationService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def rest_endpoint(self) -> NotificationRestEndpointResource:
        """Entry point for NIOS notification REST endpoint resources."""
        from ibx_nios_sdk.notification._notification_rest_endpoint import (
            NotificationRestEndpointResource,
        )

        return NotificationRestEndpointResource(self._client)

    @cached_property
    def rest_template(self) -> NotificationRestTemplateResource:
        """Entry point for NIOS notification REST template resources."""
        from ibx_nios_sdk.notification._notification_rest_template import (
            NotificationRestTemplateResource,
        )

        return NotificationRestTemplateResource(self._client)

    @cached_property
    def rule(self) -> NotificationRuleResource:
        """Entry point for NIOS notification rule resources."""
        from ibx_nios_sdk.notification._notification_rule import NotificationRuleResource

        return NotificationRuleResource(self._client)
