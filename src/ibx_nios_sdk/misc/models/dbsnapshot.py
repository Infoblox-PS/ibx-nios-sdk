# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dbsnapshot - NIOS database snapshot object.

Operations: GET collection, GET by ref, PUT (no POST/DELETE).
Functions: POST /{ref}/rollback_db_snapshot, POST /{ref}/save_db_snapshot.

WAPI type: dbsnapshot

NOTES:
- 'comment', 'timestamp', 'uuid' are read-only.
- 'rollback_db_snapshot' and 'save_db_snapshot' are nested function objects;
  typed as dict[str, Any] | None.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "timestamp",
        "uuid",
    }
)


class Dbsnapshot(BaseModel):
    """NIOS database snapshot."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    comment: str | None = Field(default=None, description="The descriptive comment.")
    timestamp: int | None = Field(
        default=None,
        description="The time when the latest OneDB snapshot was taken in Epoch seconds format.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable / function triggers ---
    rollback_db_snapshot: dict[str, Any] | None = Field(default=None)
    save_db_snapshot: dict[str, Any] | None = Field(default=None)
