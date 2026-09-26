# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupStubmember - NIOS DNS stub-member name-server group.

All 6 properties from ``components.schemas.NsgroupStubmember`` in the v2.14
DNS swagger are represented here.  The ``stub_members`` list items share the
same 6-field shape as :class:`~ibx_nios_sdk.dns.models._shared.MemberServer`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import MemberServer

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main NsgroupStubmember model
# ---------------------------------------------------------------------------


class NsgroupStubmember(BaseModel):
    """NIOS DNS stub-member name-server group configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    name: str | None = Field(
        default=None, description="The name of the Stub Member Name Server Group."
    )
    comment: str | None = Field(
        default=None,
        description="Comment for the Stub Member Name Server Group; maximum 256 characters.",
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- stub members ---
    stub_members: list[MemberServer] | None = Field(
        default=None,
        description="The Grid member servers of this stub zone. Note that the lead/stealth/grid_replicate/ preferred_primaries/override_preferred_primaries fields of the struct will be ignored when set in this field.",
    )  # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
