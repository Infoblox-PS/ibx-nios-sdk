# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dhcpfailover - NIOS DHCP failover configuration.

All 36 properties from ``components.schemas.Dhcpfailover`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "association_type",
        "ms_association_mode",
        "ms_is_conflict",
        "ms_previous_state",
        "ms_state",
        "primary_state",
        "secondary_state",
        "uuid",
    }
)


class Dhcpfailover(BaseModel):
    """NIOS DHCP failover configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    association_type: Literal["GRID", "MS"] | str | None = Field(
        default=None,
        description="The value indicating whether the failover association is Microsoft or Grid based. This is a read-only attribute.",
    )
    comment: str | None = Field(
        default=None, description="A descriptive comment about a DHCP failover object."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    failover_port: int | None = Field(
        default=None,
        description="Determines the TCP port on which the server should listen for connections from its failover peer. Valid values are between 1 and 63999.",
    )
    load_balance_split: int | None = Field(
        default=None,
        description="A load balancing split value of a DHCP failover object. Specify the value of the maximum load balancing delay in a 8-bit integer format (range from 0 to 256).",
    )
    max_client_lead_time: int | None = Field(
        default=None,
        description="The maximum client lead time value of a DHCP failover object. Specify the value of the maximum client lead time in a 32-bit integer format (range from 0 to 4294967295) that represents the duration in seconds. Valid values are between 1 and 4294967295.",
    )
    max_load_balance_delay: int | None = Field(
        default=None,
        description="The maximum load balancing delay value of a DHCP failover object. Specify the value of the maximum load balancing delay in a 32-bit integer format (range from 0 to 4294967295) that represents the duration in seconds. Valid values are between 1 and 4294967295.",
    )
    max_response_delay: int | None = Field(
        default=None,
        description="The maximum response delay value of a DHCP failover object. Specify the value of the maximum response delay in a 32-bit integer format (range from 0 to 4294967295) that represents the duration in seconds. Valid values are between 1 and 4294967295.",
    )
    max_unacked_updates: int | None = Field(
        default=None,
        description="The maximum number of unacked updates value of a DHCP failover object. Specify the value of the maximum number of unacked updates in a 32-bit integer format (range from 0 to 4294967295) that represents the number of messages. Valid values are between 1 and 4294967295.",
    )  # read-only
    ms_association_mode: Literal["RO", "RW"] | str | None = Field(
        default=None,
        description="The value that indicates whether the failover association is read-write or read-only. This is a read-only attribute.",
    )
    ms_enable_authentication: bool | None = Field(
        default=None,
        description="Determines if the authentication for the failover association is enabled or not.",
    )
    ms_enable_switchover_interval: bool | None = Field(
        default=None, description="Determines if the switchover interval is enabled or not."
    )
    ms_failover_mode: Literal["HOTSTANDBY", "LOADBALANCE"] | str | None = Field(
        default=None, description="The mode for the failover association."
    )
    ms_failover_partner: str | None = Field(
        default=None,
        description="Failover partner defined in the association with the Microsoft Server.",
    )
    ms_hotstandby_partner_role: Literal["ACTIVE", "PASSIVE"] | str | None = Field(
        default=None, description="The partner role in the case of HotStandby."
    )  # read-only
    ms_is_conflict: bool | None = Field(
        default=None,
        description="Determines if the matching Microsoft failover association (if any) is in synchronization (False) or not (True). If there is no matching failover association the returned values is False. This is a read-only attribute.",
    )
    ms_previous_state: (
        Literal[
            "INIT",
            "STARTUP",
            "RECOVER",
            "POTENTIAL_CONFLICT",
            "COMMUNICATION_INT",
            "NO_STATE",
            "NORMAL",
            "PARTNER_DOWN",
            "RESOLUTION_INIT",
            "RECOVER_DONE",
            "CONFLICT_DONE",
            "RECOVER_WAIT",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The previous failover association state. This is a read-only attribute.",
    )
    ms_server: str | None = Field(default=None, description="The primary Microsoft Server.")
    ms_shared_secret: str | None = Field(
        default=None,
        description="The failover association authentication. This is a write-only attribute.",
    )  # read-only
    ms_state: (
        Literal[
            "INIT",
            "STARTUP",
            "RECOVER",
            "POTENTIAL_CONFLICT",
            "COMMUNICATION_INT",
            "NO_STATE",
            "NORMAL",
            "PARTNER_DOWN",
            "RESOLUTION_INIT",
            "RECOVER_DONE",
            "CONFLICT_DONE",
            "RECOVER_WAIT",
        ]
        | str
        | None
    ) = Field(
        default=None, description="The failover association state. This is a read-only attribute."
    )
    ms_switchover_interval: int | None = Field(
        default=None,
        description="The time (in seconds) that DHCPv4 server will wait before transitioning the server from the COMMUNICATION-INT state to PARTNER-DOWN state.",
    )
    name: str | None = Field(default=None, description="The name of a DHCP failover object.")
    primary: str | None = Field(
        default=None, description="The primary server of a DHCP failover object."
    )
    primary_server_type: Literal["GRID", "EXTERNAL"] | str | None = Field(
        default=None,
        description="The type of the primary server of DHCP Failover association object.",
    )  # read-only
    primary_state: (
        Literal[
            "COMMUNICATIONS_INTERRUPTED",
            "RECOVER_WAIT",
            "RECOVER",
            "SHUTDOWN",
            "UNKNOWN",
            "POTENTIAL_CONFLICT",
            "NORMAL",
            "RESOLUTION_INTERRUPTED",
            "PARTNER_DOWN",
            "PAUSED",
            "RECOVER_DONE",
            "CONFLICT_DONE",
            "START",
        ]
        | str
        | None
    ) = Field(default=None, description="The primary server status of a DHCP failover object.")
    recycle_leases: bool | None = Field(
        default=None,
        description="Determines if the leases are kept in recycle bin until one week after expiration or not.",
    )
    secondary: str | None = Field(
        default=None, description="The secondary server of a DHCP failover object."
    )
    secondary_server_type: Literal["GRID", "EXTERNAL"] | str | None = Field(
        default=None,
        description="The type of the secondary server of DHCP Failover association object.",
    )  # read-only
    secondary_state: (
        Literal[
            "COMMUNICATIONS_INTERRUPTED",
            "RECOVER_WAIT",
            "RECOVER",
            "SHUTDOWN",
            "UNKNOWN",
            "POTENTIAL_CONFLICT",
            "NORMAL",
            "RESOLUTION_INTERRUPTED",
            "PARTNER_DOWN",
            "PAUSED",
            "RECOVER_DONE",
            "CONFLICT_DONE",
            "START",
        ]
        | str
        | None
    ) = Field(default=None, description="The secondary server status of a DHCP failover object.")
    set_dhcp_failover_partner_down: dict[str, Any] | None = Field(default=None)
    set_dhcp_failover_secondary_recovery: dict[str, Any] | None = Field(default=None)
    use_failover_port: bool | None = Field(default=None, description="Use flag for: failover_port")
    use_ms_switchover_interval: bool | None = Field(
        default=None, description="Use flag for: ms_switchover_interval"
    )
    use_recycle_leases: bool | None = Field(
        default=None, description="Use flag for: recycle_leases"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
