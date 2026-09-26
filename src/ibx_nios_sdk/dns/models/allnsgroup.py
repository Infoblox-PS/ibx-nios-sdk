# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Allnsgroup - NIOS DNS aggregate name-server group list (read-only).

All 4 properties from ``components.schemas.Allnsgroup`` in the v2.14 DNS
swagger are represented here.  This object is a read-only aggregate; WAPI
supports LIST only.  The ``type`` field conflicts with a Python builtin so it
is aliased as ``type_`` following the project convention.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# All non-_ref fields are read-only for this aggregate object.
# Note: the ``type`` WAPI field is stored as Python field ``type_``; the
# exclude set uses Python field names (not aliases) because WapiResource calls
# ``model_dump(exclude=_readonly_fields)``.
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "name",
        "type",
        "type_",
    }
)


# ---------------------------------------------------------------------------
# Main Allnsgroup model
# ---------------------------------------------------------------------------


class Allnsgroup(BaseModel):
    """NIOS DNS aggregate name-server group (read-only list resource).

    ``type_`` is aliased to the WAPI field ``type`` to avoid shadowing the
    Python builtin.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only identity ---
    name: str | None = Field(default=None, description="The name of the name server group.")
    comment: str | None = Field(default=None, description="The comment for the name server group.")
    type_: (
        Literal["AUTH", "FORWARDING_MEMBER", "STUB_MEMBER", "DELEGATION", "FORWARD_STUB_SERVER"]
        | str
        | None
    ) = Field(default=None, alias="type", description="Object type discriminator.")
