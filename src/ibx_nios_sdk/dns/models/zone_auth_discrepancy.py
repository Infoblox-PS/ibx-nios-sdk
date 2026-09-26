# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneAuthDiscrepancy - NIOS zone auth discrepancy (read-only aggregate).

All 6 properties from ``components.schemas.ZoneAuthDiscrepancy`` in the v2.14
DNS swagger are represented here.  This object is a read-only aggregate;
every field except ``_ref`` is marked readOnly in swagger.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# All non-_ref fields are read-only for this aggregate object.
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "description",
        "severity",
        "timestamp",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main ZoneAuthDiscrepancy model
# ---------------------------------------------------------------------------


class ZoneAuthDiscrepancy(BaseModel):
    """NIOS zone auth discrepancy (read-only aggregate).

    Provides details about discrepancies detected in authoritative zones.
    WAPI supports list/get only; create/update/delete will be rejected by WAPI.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only fields ---
    description: str | None = Field(
        default=None, description="Information about the discrepancy."
    )  # RO
    severity: Literal["CRITICAL", "SEVERE", "WARNING", "INFORMATIONAL", "NORMAL"] | str | None = (
        Field(default=None, description="The severity of the discrepancy reported.")
    )  # RO
    timestamp: int | None = Field(
        default=None,
        description="The time when the DNS integrity check was last run for this zone.",
    )  # RO
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO
    zone: str | None = Field(
        default=None,
        description="The reference of the zone during a search. Otherwise, this is the zone object of the zone to which the discrepancy refers.",
    )  # RO
