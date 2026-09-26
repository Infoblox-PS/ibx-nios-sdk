# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Orderedranges - NIOS DHCP ordered ranges aggregate.

All 3 properties from ``components.schemas.Orderedranges`` in the v2.14 DHCP
swagger are represented here.

NOTE: This is a read-only aggregate view in practice.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "network",
    }
)


class Orderedranges(BaseModel):
    """NIOS DHCP ordered ranges aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    network: str | None = Field(
        default=None, description="The reference to the network that contains ranges."
    )
    ranges: list[Any] | None = Field(
        default=None, description="The ordered list of references to ranges."
    )
