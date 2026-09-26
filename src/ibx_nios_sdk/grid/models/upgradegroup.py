# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Upgradegroup - NIOS upgrade group."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "time_zone",
        "uuid",
    }
)


class Upgradegroup(BaseModel):
    """NIOS upgrade group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(default=None, description="The upgrade group descriptive comment.")
    distribution_dependent_group: str | None = Field(
        default=None, description="The distribution dependent group name."
    )
    distribution_policy: Literal["SIMULTANEOUSLY", "SEQUENTIALLY"] | str | None = Field(
        default=None, description="The distribution scheduling policy."
    )
    distribution_time: int | None = Field(
        default=None, description="The time of the next scheduled distribution."
    )
    members: list[dict[str, object]] | None = Field(
        default=None, description="The upgrade group members."
    )
    name: str | None = Field(default=None, description="The upgrade group name.")  # read-only
    time_zone: str | None = Field(
        default=None, description="The time zone for scheduling operations."
    )
    upgrade_dependent_group: str | None = Field(
        default=None, description="The upgrade dependent group name."
    )
    upgrade_policy: Literal["SIMULTANEOUSLY", "SEQUENTIALLY"] | str | None = Field(
        default=None, description="The upgrade scheduling policy."
    )
    upgrade_time: int | None = Field(
        default=None, description="The time of the next scheduled upgrade."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
