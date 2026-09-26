# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Capacityreport - NIOS capacity report object.

Operations: GET collection, GET by ref (read-only, no POST/PUT/DELETE).

WAPI type: capacityreport

NOTES:
- All fields are read-only.
- 'object_counts' is a list of nested objects; typed as list[dict[str, Any]] | None.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "hardware_type",
        "max_capacity",
        "name",
        "object_counts",
        "percent_used",
        "role",
        "total_objects",
    }
)


class Capacityreport(BaseModel):
    """NIOS capacity report."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    hardware_type: str | None = Field(default=None, description="Hardware type of a Grid member.")
    max_capacity: int | None = Field(
        default=None, description="The maximum amount of capacity available for the Grid member."
    )
    name: str | None = Field(default=None, description="The Grid member name.")
    object_counts: list[dict[str, Any]] | None = Field(
        default=None,
        description="A list of instance counts for object types created on the Grid member.",
    )
    percent_used: int | None = Field(
        default=None, description="The percentage of the capacity in use by the Grid member."
    )
    role: str | None = Field(default=None, description="The Grid member role.")
    total_objects: int | None = Field(
        default=None, description="The total number of objects created by the Grid member."
    )
