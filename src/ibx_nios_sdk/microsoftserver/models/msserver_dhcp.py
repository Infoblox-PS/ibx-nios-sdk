# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverDhcp - NIOS MS server DHCP.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "comment",
        "dhcp_utilization",
        "dhcp_utilization_status",
        "dynamic_hosts",
        "ipv6_last_sync_ts",
        "last_sync_ts",
        "network_view",
        "read_only",
        "server_name",
        "static_hosts",
        "status",
        "status_detail",
        "status_last_updated",
        "supports_failover",
        "total_hosts",
        "uuid",
    }
)


class MsserverDhcp(BaseModel):
    """NIOS MS server DHCP."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    address: str | None = Field(
        default=None, description="The address or FQDN of the DHCP Microsoft Server."
    )
    dhcp_utilization: int | None = Field(
        default=None,
        description="The percentage of the total DHCP utilization of DHCP objects belonging to the DHCP Microsoft Server multiplied by 1000. This is the percentage of the total number of available IP addresses from all the DHCP objects belonging to the DHCP Microsoft Server versus the total number of all IP addresses in all of the DHCP objects on the DHCP Microsoft Server.",
    )
    dhcp_utilization_status: Literal["FULL", "HIGH", "LOW", "NORMAL"] | str | None = Field(
        default=None,
        description="A string describing the utilization level of DHCP objects that belong to the DHCP Microsoft Server.",
    )
    dynamic_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP leases issued for the DHCP objects on the DHCP Microsoft Server.",
    )
    ipv6_last_sync_ts: int | None = Field(
        default=None, description="Timestamp of the last synchronization attempt"
    )
    last_sync_ts: int | None = Field(
        default=None, description="Timestamp of the last synchronization attempt"
    )
    server_name: str | None = Field(default=None, description="Microsoft server address")
    static_hosts: int | None = Field(
        default=None,
        description="The number of static DHCP addresses configured in DHCP objects that belong to the DHCP Microsoft Server.",
    )
    status: (
        Literal["FAILED", "WARNING", "WORKING", "INACTIVE", "UNKNOWN", "OFFLINE"] | str | None
    ) = Field(default=None, description="Status of the Microsoft DHCP Service")
    status_detail: str | None = Field(
        default=None, description="Detailed status of the DHCP status"
    )
    status_last_updated: int | None = Field(
        default=None, description="Timestamp of the last update"
    )
    supports_failover: bool | None = Field(
        default=None, description="Flag indicating if the DHCP supports Failover"
    )
    total_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP addresses configured in DHCP objects that belong to the DHCP Microsoft Server.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(default=None, description="Comment from Microsoft Server")
    login_name: str | None = Field(
        default=None, description="The login name of the DHCP Microsoft Server."
    )
    login_password: str | None = Field(
        default=None, description="The login password of the DHCP Microsoft Server."
    )
    network_view: str | None = Field(default=None, description="Network view to update")
    next_sync_control: Literal["NONE", "START", "STOP"] | str | None = Field(
        default=None, description="Defines what control to apply on the DHCP server"
    )
    read_only: bool | None = Field(
        default=None, description="Whether Microsoft server is read only"
    )
    synchronization_interval: int | None = Field(
        default=None, description="The minimum number of minutes between two synchronizations."
    )
    use_login: bool | None = Field(
        default=None, description="Use flag for: login_name , login_password"
    )
    use_synchronization_interval: bool | None = Field(
        default=None, description="Use flag for: synchronization_interval"
    )
