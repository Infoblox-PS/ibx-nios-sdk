# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Datacollectioncluster - NIOS data collection cluster object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: datacollectioncluster

NOTES:
- 'name' and 'uuid' are read-only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "uuid",
    }
)


class Datacollectioncluster(BaseModel):
    """NIOS data collection cluster."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    name: str | None = Field(default=None, description="Display name for cluster")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    enable_registration: bool | None = Field(
        default=None, description="Enable/disable new registration requests"
    )
