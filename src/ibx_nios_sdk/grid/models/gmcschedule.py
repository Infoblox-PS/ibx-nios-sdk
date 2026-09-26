# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Gmcschedule - NIOS GMC schedule."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "gmc_groups",
        "uuid",
    }
)


class Gmcschedule(BaseModel):
    """NIOS GMC schedule."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    activate_gmc_group_schedule: bool | None = Field(
        default=None, description="Determines whether the gmc schedule is active."
    )  # read-only
    gmc_groups: list[dict[str, Any] | str] | None = Field(
        default=None, description="Object array of gmc groups"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
