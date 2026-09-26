# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ruleset - NIOS ruleset object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: ruleset

NOTES:
- 'uuid' is read-only.
- 'nxdomain_rules' is a list of nested objects; typed as list[dict[str, Any]] | None.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Ruleset(BaseModel):
    """NIOS ruleset."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="Descriptive comment about the Ruleset object."
    )
    disabled: bool | None = Field(
        default=None, description="The flag that indicates if the Ruleset object is disabled."
    )
    name: str | None = Field(default=None, description="The name of this Ruleset object.")
    nxdomain_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description='The list of Rules assigned to this Ruleset object. Rules can be set only when the Ruleset type is set to "NXDOMAIN".',
    )
    type: Literal["NXDOMAIN", "BLACKLIST"] | str | None = Field(
        default=None, description="The type of this Ruleset object."
    )
