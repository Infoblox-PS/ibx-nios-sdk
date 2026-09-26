# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Nsgroup - NIOS DNS name-server group.

All 12 properties from ``components.schemas.Nsgroup`` in the v2.14 DNS swagger
are represented here.  Nested server-list types reuse ``ExtServer`` and
``MemberServer`` from ``_shared.py`` - the shapes match exactly.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import ExtServer, MemberServer

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Nsgroup model
# ---------------------------------------------------------------------------


class Nsgroup(BaseModel):
    """NIOS DNS name-server group configuration.

    ``external_primaries`` and ``external_secondaries`` share the same 8-field
    shape as :class:`~ibx_nios_sdk.dns.models._shared.ExtServer`.
    ``grid_primary`` and ``grid_secondaries`` share the same 6-field shape as
    :class:`~ibx_nios_sdk.dns.models._shared.MemberServer`.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    name: str | None = Field(default=None, description="The name of this name server group.")
    comment: str | None = Field(
        default=None, description="Comment for the name server group; maximum 256 characters."
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- grid/external servers ---
    external_primaries: list[ExtServer] | None = Field(
        default=None, description="The list of external primary servers."
    )
    external_secondaries: list[ExtServer] | None = Field(
        default=None, description="The list of external secondary servers."
    )
    grid_primary: list[MemberServer] | None = Field(
        default=None, description="The grid primary servers for this group."
    )
    grid_secondaries: list[MemberServer] | None = Field(
        default=None,
        description="The list with Grid members that are secondary servers for this group.",
    )  # --- flags ---
    is_grid_default: bool | None = Field(
        default=None, description="Determines if this name server group is the Grid default."
    )
    is_multimaster: bool | None = Field(
        default=None,
        description='Determines if the "multiple DNS primaries" feature is enabled for the group.',
    )
    use_external_primary: bool | None = Field(
        default=None,
        description='This flag controls whether the group is using an external primary. Note that modification of this field requires passing values for "grid_secondaries" and "external_primaries".',
    )  # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
