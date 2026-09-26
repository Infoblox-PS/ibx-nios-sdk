# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DdnsPrincipalclusterGroup - NIOS DDNS principal cluster group.

All 5 properties from ``components.schemas.DdnsPrincipalclusterGroup`` in the
v2.14 DNS swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "clusters",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main DdnsPrincipalclusterGroup model
# ---------------------------------------------------------------------------


class DdnsPrincipalclusterGroup(BaseModel):
    """NIOS DDNS principal cluster group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable fields ---
    name: str | None = Field(
        default=None, description="The name of this DDNS Principal Cluster Group."
    )
    comment: str | None = Field(
        default=None, description="Comment for the DDNS Principal Cluster Group."
    )  # --- read-only fields ---
    clusters: list[str] | None = Field(
        default=None, description="The list of equivalent DDNS principal clusters."
    )  # RO - list of ddns:principalcluster refs
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO
