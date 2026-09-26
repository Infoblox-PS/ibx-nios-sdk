# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderChildren - NIOS Smart Folder children object.

Operations: GET collection, GET by ref (read-only - no POST, PUT, DELETE).

WAPI type: smartfolder:children
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "resource",
        "value",
        "value_type",
    }
)


class SmartfolderChildren(BaseModel):
    """NIOS Smart Folder children.

    NOTES:
    - 'value' is a nested structure; typed as dict[str, Any] | None.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    resource: str | None = Field(
        default=None, description="The object returned by the Smart Folder query."
    )
    value_type: (
        Literal["STRING", "INTEGER", "BOOLEAN", "DATE", "ENUM", "EMAIL", "URL", "OBJTYPE"]
        | str
        | None
    ) = Field(
        default=None, description="The type of the returned value."
    )  # --- writable / returned ---
    value: dict[str, Any] | None = Field(
        default=None, description="The value of the extensible attribute."
    )
