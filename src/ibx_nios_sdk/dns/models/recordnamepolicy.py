# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Recordnamepolicy - NIOS DNS record name policy.

All 6 properties from ``components.schemas.Recordnamepolicy`` in the v2.14
DNS swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "pre_defined",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Recordnamepolicy model
# ---------------------------------------------------------------------------


class Recordnamepolicy(BaseModel):
    """NIOS DNS record name policy."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable fields ---
    name: str | None = Field(
        default=None, description="The name of the record name policy object."
    )
    is_default: bool | None = Field(
        default=None, description="Determines whether the record name policy is Grid default."
    )
    regex: str | None = Field(
        default=None,
        description="The POSIX regular expression the record names should match in order to comply with the record name policy.",
    )  # --- read-only fields ---
    pre_defined: bool | None = Field(
        default=None, description="Determines whether the record name policy is a predefined one."
    )  # RO
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO
