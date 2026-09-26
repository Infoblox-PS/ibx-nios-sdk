# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionProfileRule - NIOS threat protection profile rule link.

All 7 properties from ``components.schemas.ThreatprotectionProfileRule`` in the
v2.14 threatprotection swagger are represented here.

Note: ``config`` is a complex nested object; approximated as
``dict[str, Any] | None`` - see NOTES.md.

Operations: GET collection + GET/PUT by ref (no POST/DELETE).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "profile",
        "rule",
        "sid",
    }
)


class ThreatprotectionProfileRule(BaseModel):
    """NIOS threat protection profile rule link.

    Links a profile to a rule. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT.

    ``config`` is approximated as ``dict[str, Any] | None`` - see NOTES.md.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    profile: str | None = Field(
        default=None, description="The name of the Threat protection profile."
    )
    rule: str | None = Field(default=None, description="The rule object name.")
    sid: int | None = Field(default=None, description="The snort rule ID.")  # --- writable ---
    config: dict[str, Any] | None = Field(
        default=None, description="Configuration block for this object."
    )
    disable: bool | None = Field(
        default=None, description="Determines if the rule is enabled or not for the profile."
    )
    use_config: bool | None = Field(default=None, description="Use flag for: config")
    use_disable: bool | None = Field(default=None, description="Use flag for: disable")
