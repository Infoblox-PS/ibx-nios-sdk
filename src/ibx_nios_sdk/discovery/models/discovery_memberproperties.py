# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryMemberproperties - NIOS discovery member properties.

Operations: GET (collection and by ref), PUT.

NOTE: Deeply nested credential/router structures → list[dict[str, Any]].
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "default_seed_routers",
        "discovery_member",
        "gateway_seed_routers",
        "is_sa",
        "role",
        "uuid",
    }
)


class DiscoveryMemberproperties(BaseModel):
    """NIOS discovery member properties."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    address: str | None = Field(default=None, description="The Grid member address IP address.")
    is_sa: bool | None = Field(
        default=None,
        description="Determines if the standalone mode for discovery network monitor is enabled or not.",
    )
    role: Literal["NONE", "DNM", "DNP"] | str | None = Field(
        default=None, description="Discovery member role."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    cli_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="Discovery CLI credentials."
    )
    default_seed_routers: list[dict[str, Any]] | None = Field(
        default=None, description="Default seed routers."
    )
    discovery_member: str | None = Field(
        default=None, description="The name of the network discovery Grid member."
    )
    enable_service: bool | None = Field(
        default=None, description="Determines if the discovery service is enabled."
    )
    gateway_seed_routers: list[dict[str, Any]] | None = Field(
        default=None, description="Gateway seed routers."
    )
    scan_interfaces: list[dict[str, Any]] | None = Field(
        default=None, description="Discovery networks to which the member is assigned."
    )
    sdn_configs: list[dict[str, Any]] | None = Field(
        default=None, description="List of SDN/SDWAN controller configurations."
    )
    seed_routers: list[dict[str, Any]] | None = Field(default=None, description="Seed routers.")
    snmpv1v2_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="Discovery SNMP v1 and v2 credentials."
    )
    snmpv3_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="Discovery SNMP v3 credentials."
    )
    use_cli_credentials: bool | None = Field(
        default=None, description="Use flag for: cli_credentials"
    )
    use_snmpv1v2_credentials: bool | None = Field(
        default=None, description="Use flag for: snmpv1v2_credentials"
    )
    use_snmpv3_credentials: bool | None = Field(
        default=None, description="Use flag for: snmpv3_credentials"
    )
