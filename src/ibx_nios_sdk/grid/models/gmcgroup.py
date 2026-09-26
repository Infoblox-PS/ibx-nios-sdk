# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Gmcgroup - NIOS GMC group."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "time_zone",
        "uuid",
    }
)


class Gmcgroup(BaseModel):
    """NIOS GMC group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(default=None, description="Description of the group")
    gmc_promotion_policy: Literal["SIMULTANEOUSLY", "SEQUENTIALLY"] | str | None = Field(
        default=None,
        description="This field decides whether the members join back at the same time or sequentially with time gap of 30 seconds.",
    )
    members: list[dict[str, object]] | None = Field(default=None, description="gmcgroup members")
    name: str | None = Field(default=None, description="Group name")
    reconnect_group_now: bool | None = Field(default=None)
    scheduled_time: int | None = Field(
        default=None, description="Absolute time at which the reconnect starts"
    )  # read-only
    time_zone: str | None = Field(
        default=None, description="The time zone for scheduling operations."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
