# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DeletedObjects - NIOS deleted objects (read-only).

Operations: GET collection, GET by ref (read-only, no POST/PUT/DELETE).

WAPI type: deleted_objects

NOTES:
- All fields are read-only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "object_type",
    }
)


class DeletedObjects(BaseModel):
    """NIOS deleted objects."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    object_type: str | None = Field(
        default=None,
        description="The object type of the deleted object. This is undefined if the object is not supported.",
    )
