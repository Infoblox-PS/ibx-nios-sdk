# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRulecategory - NIOS threat protection rule category.

All 4 properties from ``components.schemas.ThreatprotectionRulecategory`` in the
v2.14 threatprotection swagger are represented here.

Operations: GET collection + GET by ref only (no PUT/POST/DELETE - fully read-only).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - all non-_ref fields
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "is_factory_reset_enabled",
        "name",
        "ruleset",
        "uuid",
    }
)


class ThreatprotectionRulecategory(BaseModel):
    """NIOS threat protection rule category - fully read-only.

    All 4 non-``_ref`` swagger properties are present and read-only.
    Read-only fields are collected in :data:`READONLY_FIELDS`.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    is_factory_reset_enabled: bool | None = Field(
        default=None, description="Determines if factory reset is enabled for this rule category."
    )
    name: str | None = Field(default=None, description="The name of the rule category.")
    ruleset: str | None = Field(
        default=None, description="The version of the ruleset the category assigned to."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
