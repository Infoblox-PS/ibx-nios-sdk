# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Msserver - NIOS Microsoft server object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

NOTE: ad_sites, ad_user, dhcp_server, dns_server → dict[str, Any] | None
(deeply nested sub-objects).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "ad_domain",
        "connection_status",
        "connection_status_detail",
        "last_seen",
        "managing_member",
        "root_ad_domain",
        "server_name",
        "synchronization_status",
        "synchronization_status_detail",
        "uuid",
        "version",
    }
)


class Msserver(BaseModel):
    """NIOS Microsoft server."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    connection_status: str | None = Field(
        default=None, description="Result of the last RPC connection attempt made"
    )
    connection_status_detail: str | None = Field(
        default=None, description="Detail of the last connection attempt made"
    )
    last_seen: int | None = Field(
        default=None, description="Timestamp of the last message received"
    )
    synchronization_status: Literal["OK", "WARNING", "ERROR"] | str | None = Field(
        default=None, description="Synchronization status summary"
    )
    synchronization_status_detail: str | None = Field(
        default=None, description="Detail status if synchronization_status is ERROR"
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    version: str | None = Field(
        default=None, description="Version of the Microsoft Server"
    )  # --- writable ---
    ad_domain: str | None = Field(
        default=None,
        description="The Active Directory domain to which this server belongs (if applicable).",
    )
    ad_sites: dict[str, Any] | None = Field(default=None)
    ad_user: dict[str, Any] | None = Field(default=None)
    address: str | None = Field(default=None, description="The address or FQDN of the server.")
    comment: str | None = Field(
        default=None, description="User comments for this Microsoft Server"
    )
    dhcp_server: dict[str, Any] | None = Field(default=None)
    disabled: bool | None = Field(
        default=None, description="Allow/forbids usage of this Microsoft Server"
    )
    dns_server: dict[str, Any] | None = Field(default=None)
    dns_view: str | None = Field(default=None, description="Reference to the DNS view")
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    grid_member: str | None = Field(
        default=None, description="Reference to the assigned grid member"
    )
    log_destination: Literal["SYSLOG", "MSLOG"] | str | None = Field(
        default=None, description="Directs logging of sync messages either to syslog or mslog"
    )
    log_level: Literal["MINIMUM", "NORMAL", "ADVANCED", "FULL"] | str | None = Field(
        default=None, description="Log level for this Microsoft Server"
    )
    login_name: str | None = Field(
        default=None, description="Microsoft Server login name, with optional domainname"
    )
    login_password: str | None = Field(default=None, description="Microsoft Server login password")
    managing_member: str | None = Field(
        default=None, description="Hostname of grid member managing this Microsoft Server"
    )
    ms_max_connection: int | None = Field(
        default=None, description="Maximum number of connections to MS server"
    )
    ms_rpc_timeout_in_seconds: int | None = Field(
        default=None, description="Timeout in seconds of RPC connections for this MS Server"
    )
    network_view: str | None = Field(default=None, description="Reference to the network view")
    read_only: bool | None = Field(
        default=None, description="Enable read-only management for this Microsoft Server"
    )
    root_ad_domain: str | None = Field(
        default=None,
        description="The root Active Directory domain to which this server belongs (if applicable).",
    )
    server_name: str | None = Field(
        default=None, description="Gives the server name as reported by itself"
    )
    synchronization_min_delay: int | None = Field(
        default=None, description="Minimum number of minutes between two synchronizations"
    )
    use_log_destination: bool | None = Field(
        default=None, description="Override log_destination inherited from grid level"
    )
    use_ms_max_connection: bool | None = Field(
        default=None, description="Override grid ms_max_connection setting"
    )
    use_ms_rpc_timeout_in_seconds: bool | None = Field(
        default=None, description="Flag to override cluster RPC timeout"
    )
