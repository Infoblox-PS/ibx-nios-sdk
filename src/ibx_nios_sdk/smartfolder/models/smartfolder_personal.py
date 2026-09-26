# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderPersonal - NIOS personal Smart Folder object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: smartfolder:personal
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "is_shortcut",
    }
)


class SmartfolderPersonal(BaseModel):
    """NIOS personal Smart Folder.

    NOTES:
    - 'group_bys', 'query_items', 'save_as' are nested structures; typed as
      list[dict[str, Any]] | None and dict[str, Any] | None respectively.
    - 'is_shortcut' is read-only per swagger schema.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    is_shortcut: bool | None = Field(
        default=None, description="Determines whether the personal Smart Folder is a shortcut."
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The personal Smart Folder descriptive comment."
    )
    group_bys: list[dict[str, Any]] | None = Field(
        default=None, description="The personal Smart Folder grouping rules."
    )
    name: str | None = Field(default=None, description="The personal Smart Folder name.")
    query_items: list[dict[str, Any]] | None = Field(
        default=None, description="The personal Smart Folder filter queries."
    )
    save_as: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the save-as operation."
    )
