# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6dhcpoptionspace - NIOS DHCP IPv6 option space.

All 6 properties from ``components.schemas.Ipv6dhcpoptionspace`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Ipv6dhcpoptionspace(BaseModel):
    """NIOS DHCP IPv6 option space."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="A descriptive comment of a DHCP IPv6 option space object."
    )
    enterprise_number: int | None = Field(
        default=None, description="The enterprise number of a DHCP IPv6 option space object."
    )
    name: str | None = Field(
        default=None, description="The name of a DHCP IPv6 option space object."
    )
    option_definitions: list[str] | None = Field(
        default=None, description="The list of DHCP IPv6 option definition objects."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
