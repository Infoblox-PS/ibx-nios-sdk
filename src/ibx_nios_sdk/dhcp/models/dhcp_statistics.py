# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpStatistics - NIOS DHCP statistics (read-only aggregate).

All 5 properties from ``components.schemas.DhcpStatistics`` in the v2.14 DHCP
swagger are represented here.

NOTE: _wapi_type is ``dhcp:statistics`` (colon in type string).

NOTE: This is a read-only aggregate view in practice; WAPI will reject
write attempts. No SDK enforcement - callers are responsible.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "dhcp_utilization",
        "dhcp_utilization_status",
        "dynamic_hosts",
        "static_hosts",
        "total_hosts",
    }
)


class DhcpStatistics(BaseModel):
    """NIOS DHCP statistics aggregate view."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    dhcp_utilization: int | None = Field(
        default=None,
        description="The percentage of the total DHCP utilization of DHCP objects multiplied by 1000. This is the percentage of the total number of available IP addresses belonging to the object versus the total number of all IP addresses in object.",
    )
    dhcp_utilization_status: Literal["FULL", "HIGH", "LOW", "NORMAL"] | str | None = Field(
        default=None, description="A string describing the utilization level of the DHCP object."
    )
    dynamic_hosts: int | None = Field(
        default=None, description="The total number of DHCP leases issued for the DHCP object."
    )
    static_hosts: int | None = Field(
        default=None,
        description="The number of static DHCP addresses configured in the DHCP object.",
    )
    total_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP addresses configured in the DHCP object.",
    )
