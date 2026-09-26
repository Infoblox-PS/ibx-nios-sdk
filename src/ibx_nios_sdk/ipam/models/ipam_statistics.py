# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""IpamStatistics - NIOS IPAM statistics aggregate view.

All 9 properties from ``components.schemas.IpamStatistics`` in the v2.14
IPAM swagger are represented here.

NOTE: _wapi_type is ``ipam:statistics`` (colon in type string).
The snake accessor on IpamService is ``ipam_statistics``.

NOTE: This is a read-only aggregate view in practice; WAPI will reject
write attempts. No SDK enforcement - callers are responsible.

NOTE: The following complex nested schemas are inlined as dicts:
  - IpamStatisticsMsAdUserData
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cidr",
        "conflict_count",
        "ms_ad_user_data",
        "network",
        "network_view",
        "unmanaged_count",
        "utilization",
        "utilization_update",
    }
)


# ---------------------------------------------------------------------------
# Main IpamStatistics model
# ---------------------------------------------------------------------------


class IpamStatistics(BaseModel):
    """NIOS IPAM statistics aggregate view.

    All 9 swagger properties are present. All substantive fields are read-only
    (collected in :data:`READONLY_FIELDS`); the resource strips them before
    PUT/POST. In practice WAPI will reject write attempts.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    cidr: int | None = Field(default=None, description="The network CIDR.")
    conflict_count: int | None = Field(
        default=None,
        description="The number of conflicts discovered via network discovery. This attribute is only valid for a Network object.",
    )  # --- MS AD user data (complex nested - dict) ---
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- read-only ---
    network: str | None = Field(default=None, description="The network address.")
    network_view: str | None = Field(default=None, description="The network view.")
    unmanaged_count: int | None = Field(
        default=None,
        description="The number of unmanaged IP addresses as discovered by network discovery. This attribute is only valid for a Network object.",
    )
    utilization: int | None = Field(
        default=None, description="The network utilization in percentage."
    )
    utilization_update: int | None = Field(
        default=None,
        description="The time that the utilization statistics were updated last. This attribute is only valid for a Network object. For a Network Container object, the return value is undefined.",
    )
