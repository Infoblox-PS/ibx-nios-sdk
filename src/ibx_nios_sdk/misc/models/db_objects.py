# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DbObjects - NIOS database objects (read-only).

Operations: GET collection, GET by ref (read-only, no POST/PUT/DELETE).

WAPI type: db_objects

NOTES:
- All fields are read-only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "last_sequence_id",
        "object",
        "object_type",
        "unique_id",
    }
)


class DbObjects(BaseModel):
    """NIOS database objects."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    last_sequence_id: str | None = Field(
        default=None, description="The last returned sequence ID."
    )
    object: str | None = Field(
        default=None,
        description='The record object when supported by WAPI. Otherwise, the value is "None".',
    )
    object_type: str | None = Field(
        default=None,
        description="The object type. This is undefined if the object is not supported.",
    )
    unique_id: str | None = Field(
        default=None, description="The unique ID of the requested object."
    )
