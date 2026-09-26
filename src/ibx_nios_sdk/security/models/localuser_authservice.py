# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LocaluserAuthservice - NIOS local user authentication service (read-only singleton).

All 4 properties from ``components.schemas.LocaluserAuthservice`` in the v2.14
security swagger are represented here. All non-_ref fields are readOnly -
this is a built-in singleton for the NIOS local user authentication service.

Operations: GET collection, GET by ref, PUT (singleton with readOnly fields -
no POST/DELETE at WAPI level).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "disabled",
        "name",
    }
)


class LocaluserAuthservice(BaseModel):
    """NIOS local user authentication service (singleton).

    All non-_ref fields are read-only. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    comment: str | None = Field(
        default=None, description="The local user authentication service comment."
    )
    disabled: bool | None = Field(
        default=None,
        description="Flag that indicates whether the local user authentication service is enabled or not.",
    )
    name: str | None = Field(
        default=None, description="The name of the local user authentication service."
    )
