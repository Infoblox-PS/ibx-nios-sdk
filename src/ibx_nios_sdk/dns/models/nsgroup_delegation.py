# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupDelegation - NIOS DNS delegation name-server group.

All 6 properties from ``components.schemas.NsgroupDelegation`` in the v2.14
DNS swagger are represented here.  The ``delegate_to`` list items share the
same 8-field shape as :class:`~ibx_nios_sdk.dns.models._shared.ExtServer`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import ExtServer

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main NsgroupDelegation model
# ---------------------------------------------------------------------------


class NsgroupDelegation(BaseModel):
    """NIOS DNS delegation name-server group configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    name: str | None = Field(default=None, description="The name of the delegated NS group.")
    comment: str | None = Field(
        default=None, description="The comment for the delegated NS group."
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- delegation targets ---
    delegate_to: list[ExtServer] | None = Field(
        default=None, description="The list of delegated servers for the delegated NS group."
    )  # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
