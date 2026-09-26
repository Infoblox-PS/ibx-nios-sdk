# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionGridRule - NIOS grid-level threat protection rule.

All 13 properties from ``components.schemas.ThreatprotectionGridRule`` in the
v2.14 threatprotection swagger are represented here.

Note: ``config`` is a complex nested object (``ThreatprotectionGridRuleConfig``)
with a ``params`` array of structured entries. Approximated as
``dict[str, Any] | None`` - see NOTES.md.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "allowed_actions",
        "category",
        "description",
        "is_factory_reset_enabled",
        "name",
        "ruleset",
        "sid",
        "type_",
        "uuid",
    }
)


class ThreatprotectionGridRule(BaseModel):
    """NIOS grid-level threat protection rule.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.

    ``type`` (Python keyword collision) is exposed as ``type_`` with
    ``Field(alias="type")``.

    ``config`` is approximated as ``dict[str, Any] | None`` - see NOTES.md.
    ``allowed_actions`` is an array of strings.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    allowed_actions: list[Literal["ALERT", "PASS", "DROP"] | str] | None = Field(
        default=None, description="The list of allowed actions of the custom rule."
    )
    category: str | None = Field(
        default=None, description="The rule category the custom rule assigned to."
    )
    description: str | None = Field(
        default=None, description="The description of the custom rule."
    )
    is_factory_reset_enabled: bool | None = Field(
        default=None, description="Determines if factory reset is enabled for the custom rule."
    )
    name: str | None = Field(
        default=None,
        description="The name of the rule custom rule concatenated with its rule config parameters.",
    )
    ruleset: str | None = Field(
        default=None, description="The version of the ruleset the custom rule assigned to."
    )
    sid: int | None = Field(
        default=None, description="The Rule ID."
    )  # --- Python keyword collision: type → type_ ---
    type_: Literal["SYSTEM", "AUTO", "CUSTOM"] | str | None = Field(
        default=None, alias="type", description="Object type discriminator."
    )

    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The human readable comment for the custom rule."
    )  # --- approximated nested config ---
    config: dict[str, Any] | None = Field(
        default=None, description="Configuration block for this object."
    )
    disabled: bool | None = Field(
        default=None, description="Determines if the rule is enabled or not for the profile."
    )
    template: str | None = Field(
        default=None, description="The threat protection rule template used to create this rule."
    )
