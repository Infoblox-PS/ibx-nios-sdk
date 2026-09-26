# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberParentalcontrol - NIOS member parental control service."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "uuid",
    }
)


class MemberParentalcontrol(BaseModel):
    """NIOS member parental control service."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    enable_service: bool | None = Field(
        default=None, description="Determines if the parental control service is enabled."
    )  # read-only
    name: str | None = Field(
        default=None, description="The parental control member hostname."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
