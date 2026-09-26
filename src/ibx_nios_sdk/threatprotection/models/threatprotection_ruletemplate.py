# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRuletemplate - NIOS threat protection rule template.

All 9 properties from ``components.schemas.ThreatprotectionRuletemplate`` in the
v2.14 threatprotection swagger are represented here.

Operations: GET collection + GET by ref only (no PUT/POST/DELETE - fully read-only).

Note: ``default_config`` is a complex nested object; approximated as
``dict[str, Any] | None`` - see NOTES.md.
``allowed_actions`` is an array of strings.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - all non-_ref fields
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "allowed_actions",
        "category",
        "default_config",
        "description",
        "name",
        "ruleset",
        "sid",
        "uuid",
    }
)


class ThreatprotectionRuletemplate(BaseModel):
    """NIOS threat protection rule template - fully read-only.

    All 8 non-``_ref`` swagger properties are present and read-only.
    Read-only fields are collected in :data:`READONLY_FIELDS`.

    ``default_config`` is approximated as ``dict[str, Any] | None`` - see NOTES.md.
    ``allowed_actions`` is an array of strings.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    allowed_actions: list[Literal["ALERT", "PASS", "DROP"] | str] | None = Field(
        default=None, description="The list of allowed actions of rhe rule template."
    )
    category: str | None = Field(
        default=None, description="The rule category this template assigned to."
    )
    description: str | None = Field(
        default=None, description="The description of the rule template."
    )
    name: str | None = Field(default=None, description="The name of the rule template.")
    ruleset: str | None = Field(
        default=None, description="The version of the ruleset the template assigned to."
    )
    sid: int | None = Field(default=None, description="The Rule ID.")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- approximated nested config (read-only in practice) ---
    default_config: dict[str, Any] | None = Field(default=None)
