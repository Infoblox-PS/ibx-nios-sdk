# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRule - NIOS notification rule object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: notification:rule

NOTES:
- 'publish_settings', 'scheduled_event', 'template_instance',
  'trigger_outbound' are deeply-nested structures; typed as dict[str, Any] | None.
- 'expression_list', 'event_deduplication_fields', 'selected_members'
  are list fields.
- 'uuid' is read-only.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class NotificationRule(BaseModel):
    """NIOS notification rule."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    all_members: bool | None = Field(
        default=None,
        description="Determines whether the notification rule is applied on all members or not. When this is set to False, the notification rule is applied only on selected_members.",
    )
    comment: str | None = Field(
        default=None, description="The notification rule descriptive comment."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a notification rule is disabled or not. When this is set to False, the notification rule is enabled.",
    )
    enable_event_deduplication: bool | None = Field(
        default=None,
        description="Determines whether the notification rule for event deduplication is enabled. Note that to enable event deduplication, you must set at least one deduplication field.",
    )
    enable_event_deduplication_log: bool | None = Field(
        default=None,
        description="Determines whether the notification rule for the event deduplication syslog is enabled.",
    )
    event_deduplication_fields: (
        list[
            Literal[
                "DXL_TOPIC",
                "DISCOVERER",
                "DUID",
                "IP_ADDRESS",
                "MAC_ADDRESS",
                "NETWORK",
                "NETWORK_VIEW",
                "QUERY_FQDN",
                "QUERY_NAME",
                "QUERY_TYPE",
                "RPZ_POLICY",
                "RPZ_TYPE",
                "RULE_ACTION",
                "RULE_CATEGORY",
                "RULE_SEVERITY",
                "RULE_SID",
                "SOURCE_IP",
                "SOURCE_PORT",
                "OPERATION_TYPE",
            ]
            | str
        ]
        | None
    ) = Field(
        default=None,
        description="The list of fields that must be used in the notification rule for event deduplication.",
    )
    event_deduplication_lookback_period: int | None = Field(
        default=None,
        description="The lookback period for the notification rule for event deduplication.",
    )
    event_priority: str | None = Field(default=None, description="Event priority.")
    event_type: (
        Literal[
            "DXL_EVENT_SUBSCRIBER",
            "DB_CHANGE_DNS_RECORD",
            "DB_CHANGE_DNS_ZONE",
            "DNS_RPZ",
            "DHCP_LEASES",
            "SECURITY_ADP",
            "IPAM",
            "ANALYTICS_DNS_TUNNEL",
            "DB_CHANGE_DHCP_FIXED_ADDRESS_IPV4",
            "DB_CHANGE_DHCP_FIXED_ADDRESS_IPV6",
            "DB_CHANGE_DHCP_NETWORK_IPV4",
            "DB_CHANGE_DHCP_NETWORK_IPV6",
            "DB_CHANGE_DHCP_RANGE_IPV4",
            "DB_CHANGE_DHCP_RANGE_IPV6",
            "DB_CHANGE_DNS_HOST_ADDRESS_IPV4",
            "DB_CHANGE_DNS_HOST_ADDRESS_IPV6",
            "DB_CHANGE_DNS_DISCOVERY_DATA",
            "SCHEDULE",
        ]
        | str
        | None
    ) = Field(default=None, description="The notification rule event type.")
    expression_list: list[dict[str, Any]] | None = Field(
        default=None, description="The notification rule expression list."
    )
    name: str | None = Field(default=None, description="The notification rule name.")
    notification_action: (
        Literal["CISCOISE_QUARANTINE", "CISCOISE_PUBLISH", "RESTAPI_TEMPLATE_INSTANCE"]
        | str
        | None
    ) = Field(
        default=None,
        description="The notification rule action is applied if expression list evaluates to True.",
    )
    notification_target: str | None = Field(default=None, description="The notification target.")
    publish_settings: dict[str, Any] | None = Field(
        default=None, description="Publish settings for outbound updates."
    )
    scheduled_event: dict[str, Any] | None = Field(default=None)
    selected_members: list[str] | None = Field(
        default=None,
        description="The list of the members on which the notification rule is applied.",
    )
    template_instance: dict[str, Any] | None = Field(
        default=None, description="Reference to the template this object was instantiated from."
    )
    trigger_outbound: dict[str, Any] | None = Field(default=None)
    use_publish_settings: bool | None = Field(
        default=None, description="Use flag for: publish_settings"
    )
