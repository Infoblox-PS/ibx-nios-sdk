# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridDashboard - NIOS Grid dashboard thresholds.

All properties from ``components.schemas.GridDashboard`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class GridDashboard(BaseModel):
    """NIOS Grid dashboard thresholds."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    analytics_tunneling_event_critical_threshold: int | None = Field(
        default=None,
        description="The Grid Dashboard critical threshold for Analytics tunneling events.",
    )
    analytics_tunneling_event_warning_threshold: int | None = Field(
        default=None,
        description="The Grid Dashboard warning threshold for Analytics tunneling events.",
    )
    atp_critical_event_critical_threshold: int | None = Field(
        default=None, description="The Grid Dashboard critical threshold for ATP critical events."
    )
    atp_critical_event_warning_threshold: int | None = Field(
        default=None, description="The Grid Dashboard warning threshold for ATP critical events."
    )
    atp_major_event_critical_threshold: int | None = Field(
        default=None, description="The Grid Dashboard critical threshold for ATP major events."
    )
    atp_major_event_warning_threshold: int | None = Field(
        default=None, description="The Grid Dashboard warning threshold for ATP major events."
    )
    atp_warning_event_critical_threshold: int | None = Field(
        default=None, description="The Grid Dashboard critical threshold for ATP warning events."
    )
    atp_warning_event_warning_threshold: int | None = Field(
        default=None, description="The Grid Dashboard warning threshold for ATP warning events."
    )
    rpz_blocked_hit_critical_threshold: int | None = Field(
        default=None,
        description="The critical threshold value for blocked RPZ hits in the Grid dashboard.",
    )
    rpz_blocked_hit_warning_threshold: int | None = Field(
        default=None,
        description="The warning threshold value for blocked RPZ hits in the Grid dashboard.",
    )
    rpz_passthru_event_critical_threshold: int | None = Field(
        default=None, description="The Grid Dashboard critical threshold for RPZ passthru events."
    )
    rpz_passthru_event_warning_threshold: int | None = Field(
        default=None, description="The Grid Dashboard warning threshold for RPZ passthru events."
    )
    rpz_substituted_hit_critical_threshold: int | None = Field(
        default=None,
        description="The critical threshold value for substituted RPZ hits in the Grid dashboard.",
    )
    rpz_substituted_hit_warning_threshold: int | None = Field(
        default=None,
        description="The warning threshold value for substituted RPZ hits in the Grid dashboard.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
