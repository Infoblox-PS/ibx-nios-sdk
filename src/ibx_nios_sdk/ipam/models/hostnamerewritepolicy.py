# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Hostnamerewritepolicy - NIOS IPAM hostname rewrite policy object.

All 7 properties from ``components.schemas.Hostnamerewritepolicy`` in the
v2.14 IPAM swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "is_default",
        "pre_defined",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Hostnamerewritepolicy model
# ---------------------------------------------------------------------------


class Hostnamerewritepolicy(BaseModel):
    """NIOS IPAM hostname rewrite policy object.

    All 7 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    is_default: bool | None = Field(
        default=None, description="True if the policy is the Grid default."
    )  # --- identity ---
    name: str | None = Field(
        default=None, description="The name of a hostname rewrite policy object."
    )  # --- read-only ---
    pre_defined: bool | None = Field(
        default=None, description="Determines whether the policy is a predefined one."
    )  # --- character config ---
    replacement_character: str | None = Field(
        default=None,
        description="The replacement character for symbols in hostnames that do not conform to the hostname policy.",
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- character config ---
    valid_characters: str | None = Field(
        default=None, description="The set of valid characters represented in string format."
    )  # --- scripts ---
