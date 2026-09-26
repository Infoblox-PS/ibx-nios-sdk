# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceneighbor - NIOS discovered device neighbor (read-only).

Operations: GET (collection and by ref) only.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "address_ref",
        "device",
        "interface",
        "mac",
        "name",
        "vlan_infos",
    }
)


class DiscoveryDeviceneighbor(BaseModel):
    """NIOS discovered device neighbor - read-only aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    address: str | None = Field(
        default=None, description="The IPv4 Address or IPv6 Address of the device neighbor."
    )
    address_ref: str | None = Field(
        default=None, description="The ref to the management IP address of the device neighbor."
    )
    device: str | None = Field(
        default=None, description="The ref to the device to which the device neighbor belongs."
    )
    interface: str | None = Field(
        default=None, description="The ref to the interface to which the device neighbor belongs."
    )
    mac: str | None = Field(default=None, description="The MAC address of the device neighbor.")
    name: str | None = Field(default=None, description="The name of the device neighbor.")
    vlan_infos: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of VLAN information associated with the device neighbor.",
    )
