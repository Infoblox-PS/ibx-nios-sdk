# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Upgradeschedule - NIOS upgrade schedule."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "time_zone",
    }
)


class Upgradeschedule(BaseModel):
    """NIOS upgrade schedule."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    active: bool | None = Field(
        default=None, description="Determines whether the upgrade schedule is active."
    )
    start_time: int | None = Field(
        default=None, description="The start time of the upgrade."
    )  # read-only
    time_zone: str | None = Field(
        default=None, description="The time zone for upgrade start time."
    )
    upgrade_groups: list[dict[str, object]] | None = Field(
        default=None, description="The upgrade groups scheduling settings."
    )
