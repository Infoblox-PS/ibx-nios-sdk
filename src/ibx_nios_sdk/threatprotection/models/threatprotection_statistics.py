# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionStatistics - NIOS threat protection statistics.

All 2 properties from ``components.schemas.ThreatprotectionStatistics`` in the
v2.14 threatprotection swagger are represented here.

Operations: GET collection + GET by ref only (no PUT/POST/DELETE - fully read-only).

Note: ``stat_infos`` is an array of ``ThreatprotectionStatisticsStatInfos`` objects;
approximated as ``list[dict[str, Any]] | None`` - see NOTES.md.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - all non-_ref fields
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "member",
        "stat_infos",
    }
)


class ThreatprotectionStatistics(BaseModel):
    """NIOS threat protection statistics - fully read-only.

    Both non-``_ref`` swagger properties are read-only.
    Read-only fields are collected in :data:`READONLY_FIELDS`.

    ``stat_infos`` is approximated as ``list[dict[str, Any]] | None`` - see NOTES.md.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    member: str | None = Field(
        default=None,
        description="The Grid member name to get threat protection statistics. If nothing is specified then event statistics is returned for the Grid.",
    )
    stat_infos: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of event statistical information for the Grid or particular members.",
    )
