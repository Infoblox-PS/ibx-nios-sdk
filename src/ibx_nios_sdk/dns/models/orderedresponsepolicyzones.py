# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Orderedresponsepolicyzones - NIOS ordered response policy zones.

All 4 properties from ``components.schemas.Orderedresponsepolicyzones`` in
the v2.14 DNS swagger are represented here.  ``rp_zones`` is an ordered list
of zone_rp ``_ref`` strings.
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


# ---------------------------------------------------------------------------
# Main Orderedresponsepolicyzones model
# ---------------------------------------------------------------------------


class Orderedresponsepolicyzones(BaseModel):
    """NIOS ordered response policy zones.

    ``rp_zones`` is an ordered list of zone_rp ``_ref`` strings that defines
    the evaluation order for response policy zones in a given view.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable fields ---
    view: str | None = Field(default=None, description="The DNS View name.")
    rp_zones: list[str] | None = Field(
        default=None, description="An ordered list of Response Policy Zone names."
    )  # ordered list of zone_rp _ref strings

    # --- read-only fields ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO
