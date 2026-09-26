# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoverySdnnetwork - NIOS discovery SDN network (read-only).

Operations: GET (collection and by ref) only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "first_seen",
        "name",
        "network_view",
        "source_sdn_config",
    }
)


class DiscoverySdnnetwork(BaseModel):
    """NIOS discovery SDN network - read-only aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    first_seen: int | None = Field(
        default=None, description="Timestamp when this SDN network was first discovered."
    )
    name: str | None = Field(default=None, description="The name of the SDN network.")
    network_view: str | None = Field(
        default=None, description="The name of the network view assigned to this SDN network."
    )
    source_sdn_config: str | None = Field(
        default=None, description="Name of SDN configuration this network belongs to."
    )
