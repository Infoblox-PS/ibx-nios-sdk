# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dhcpoptionspace - NIOS DHCP option space.

All 6 properties from ``components.schemas.Dhcpoptionspace`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "space_type",
        "uuid",
    }
)


class Dhcpoptionspace(BaseModel):
    """NIOS DHCP option space."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="A descriptive comment of a DHCP option space object."
    )
    name: str | None = Field(default=None, description="The name of a DHCP option space object.")
    option_definitions: list[str] | None = Field(
        default=None, description="The list of DHCP option definition objects."
    )  # read-only
    space_type: Literal["PREDEFINED_DHCP", "VENDOR_SPACE"] | str | None = Field(
        default=None, description="The type of a DHCP option space object."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
