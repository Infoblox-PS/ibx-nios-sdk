# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Mastergrid - NIOS Master Grid (GMC) settings."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "connection_disabled",
        "connection_timestamp",
        "detached",
        "join_status",
        "join_token",
        "join_token_expiration",
        "joined",
        "last_event",
        "last_event_details",
        "last_sync_timestamp",
        "mgm_communication_mode",
        "use_mgmt_port",
        "uuid",
    }
)


class Mastergrid(BaseModel):
    """NIOS Master Grid (GMC) settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    address: str | None = Field(
        default=None, description="IP Address or FQDN to use to contact the SGM"
    )  # read-only
    connection_disabled: bool | None = Field(
        default=None,
        description="Indicates whether the sub-grid is currently disabled (true) or not (false).",
    )  # read-only
    connection_timestamp: int | None = Field(
        default=None,
        description="Timestamp of the beginning of the current VPN connection with the SGM.",
    )  # read-only
    detached: bool | None = Field(
        default=None, description="Indicate detached state of subgrid with MGM."
    )
    discovery_sync_disabled: bool | None = Field(
        default=None, description="Enable/Disable discovery service."
    )
    enable: bool | None = Field(
        default=None, description="Enable/Disable SuperGrid membership feature"
    )  # read-only
    join_status: Literal["FAILED", "WARNING", "WORKING", "INACTIVE"] | str | None = Field(
        default=None, description="Gives the overall status of the Super Grid connectivity"
    )  # read-only
    join_token: str | None = Field(
        default=None, description="Sub grid join token value."
    )  # read-only
    join_token_expiration: int | None = Field(
        default=None, description="Timestamp when the sub grid join token expires."
    )  # read-only
    joined: bool | None = Field(
        default=None, description="Indicates whether the sub-grid is currently joined or not."
    )  # read-only
    last_event: Literal["EVICT", "DISABLE", "MESSAGE", "ATTACH", "DETACH"] | str | None = Field(
        default=None, description="Last event notified by the Super Grid Master."
    )  # read-only
    last_event_details: str | None = Field(
        default=None, description="additional details on the event."
    )  # read-only
    last_sync_timestamp: int | None = Field(
        default=None, description="Timestamp of the last synchronization with the SGM."
    )  # read-only
    mgm_communication_mode: Literal["MODE1", "MODE2"] | str | None = Field(
        default=None, description="MGM Communication Mode."
    )
    port: int | None = Field(
        default=None,
        description="Alternate port number to use when connecting to the VPN endpoint.",
    )  # read-only
    use_mgmt_port: bool | None = Field(
        default=None,
        description="Indicates whether to use the management port to connect to the SGM.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
