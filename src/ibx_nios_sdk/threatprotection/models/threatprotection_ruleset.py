# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRuleset - NIOS threat protection ruleset.

All 8 properties from ``components.schemas.ThreatprotectionRuleset`` in the
v2.14 threatprotection swagger are represented here.

``used_by`` is an array; approximated as ``list[str] | None`` - see NOTES.md.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "add_type",
        "added_time",
        "is_factory_reset_enabled",
        "used_by",
        "uuid",
        "version",
    }
)


class ThreatprotectionRuleset(BaseModel):
    """NIOS threat protection ruleset.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.

    ``used_by`` is approximated as ``list[str] | None`` - see NOTES.md.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    add_type: Literal["AUTOMATIC", "MANUAL"] | str | None = Field(
        default=None, description="Determines the way the ruleset was added."
    )
    added_time: int | None = Field(
        default=None, description="The time when the ruleset was added."
    )
    is_factory_reset_enabled: bool | None = Field(
        default=None, description="Determines if factory reset is enabled for this ruleset."
    )
    used_by: list[str] | None = Field(default=None, description="The users of the ruleset.")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    version: str | None = Field(
        default=None, description="The ruleset version."
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The human readable comment for the ruleset."
    )
    do_not_delete: bool | None = Field(
        default=None, description="Determines if the ruleset will not be deleted during upgrade."
    )
