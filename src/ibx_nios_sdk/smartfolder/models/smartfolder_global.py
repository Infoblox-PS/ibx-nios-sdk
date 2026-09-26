# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderGlobal - NIOS global Smart Folder object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: smartfolder:global
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class SmartfolderGlobal(BaseModel):
    """NIOS global Smart Folder.

    NOTES:
    - 'group_bys', 'query_items', 'save_as' are nested structures; typed as
      list[dict[str, Any]] | None and dict[str, Any] | None respectively.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The global Smart Folder descriptive comment."
    )
    group_bys: list[dict[str, Any]] | None = Field(
        default=None, description="Global Smart Folder grouping rules."
    )
    name: str | None = Field(default=None, description="The global Smart Folder name.")
    query_items: list[dict[str, Any]] | None = Field(
        default=None, description="The global Smart Folder filter queries."
    )
    save_as: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the save-as operation."
    )
