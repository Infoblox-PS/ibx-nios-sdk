# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupForwardstubserver - NIOS DNS forward/stub-server name-server group.

All 6 properties from ``components.schemas.NsgroupForwardstubserver`` in the
v2.14 DNS swagger are represented here.  The ``external_servers`` list items
share the same 8-field shape as
:class:`~ibx_nios_sdk.dns.models._shared.ExtServer`.
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
# Main NsgroupForwardstubserver model
# ---------------------------------------------------------------------------


class NsgroupForwardstubserver(BaseModel):
    """NIOS DNS forward/stub-server name-server group configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    name: str | None = Field(
        default=None, description="The name of this Forward Stub Server Name Server Group."
    )
    comment: str | None = Field(
        default=None,
        description="Comment for the Forward Stub Server Name Server Group; maximum 256 characters.",
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- external servers ---
    external_servers: list[ExtServer] | None = Field(
        default=None, description="The list of external servers."
    )  # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
