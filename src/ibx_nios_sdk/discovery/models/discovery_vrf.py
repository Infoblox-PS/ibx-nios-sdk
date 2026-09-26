# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryVrf - NIOS discovery VRF (read-only).

Operations: GET (collection and by ref) only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "description",
        "device",
        "name",
        "network_view",
        "route_distinguisher",
    }
)


class DiscoveryVrf(BaseModel):
    """NIOS discovery VRF - read-only aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    description: str | None = Field(
        default=None, description="Additional information about the VRF."
    )
    device: str | None = Field(default=None, description="The device to which the VRF belongs.")
    name: str | None = Field(default=None, description="The name of the VRF.")
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this VRF resides."
    )
    route_distinguisher: str | None = Field(
        default=None, description="The route distinguisher associated with the VRF."
    )
