# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRestTemplate - NIOS notification REST template object.

Operations: GET collection, GET by ref, PUT, DELETE (no POST - templates are system-generated).

WAPI type: notification:rest:template

NOTES:
- 'action_name', 'added_on', 'event_type', 'outbound_type', 'parameters',
  'template_type', 'uuid', 'vendor_identifier' are read-only.
- 'parameters' is typed as list[dict[str, Any]] | None (nested structure).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "action_name",
        "added_on",
        "event_type",
        "outbound_type",
        "parameters",
        "template_type",
        "uuid",
        "vendor_identifier",
    }
)


class NotificationRestTemplate(BaseModel):
    """NIOS notification REST template.

    NOTES:
    - 'event_type' and 'parameters' are read-only list fields.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    action_name: str | None = Field(default=None, description="The action name.")
    added_on: int | None = Field(
        default=None, description="The time stamp when a template was added."
    )
    event_type: (
        list[
            Literal[
                "DNS_RPZ",
                "DHCP_LEASE",
                "ANALYTICS_DNS_TUNNEL",
                "SECURITY_ADP",
                "SCHEDULE",
                "SESSION",
                "DXL_EVENT_SUBSCRIBER",
                "DB_CHANGE_DHCP_NETWORK_IPV4",
                "DB_CHANGE_DHCP_NETWORK_IPV6",
                "DB_CHANGE_DHCP_RANGE_IPV4",
                "DB_CHANGE_DHCP_RANGE_IPV6",
                "DB_CHANGE_DHCP_FIXED_ADDRESS_IPV4",
                "DB_CHANGE_DHCP_FIXED_ADDRESS_IPV6",
                "DB_CHANGE_DNS_HOST_ADDRESS_IPV4",
                "DB_CHANGE_DNS_HOST_ADDRESS_IPV6",
                "DB_CHANGE_DNS_DISCOVERY_DATA",
                "DB_CHANGE_DNS_RECORD",
                "DB_CHANGE_DNS_ZONE",
            ]
            | str
        ]
        | None
    ) = Field(default=None, description="The event type.")
    outbound_type: Literal["DXL", "REST", "SYSLOG"] | str | None = Field(
        default=None, description="The outbound type for the template."
    )
    parameters: list[dict[str, Any]] | None = Field(
        default=None, description="The notification REST template parameters."
    )
    template_type: Literal["REST_ENDPOINT", "REST_EVENT"] | str | None = Field(
        default=None, description="The template type."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    vendor_identifier: str | None = Field(
        default=None, description="The vendor identifier."
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The comment for this REST API template."
    )
    content: str | None = Field(
        default=None,
        description="The JSON formatted content of a template. The data passed by content creates parameters for a template.",
    )
    name: str | None = Field(default=None, description="The name of a notification REST template.")
