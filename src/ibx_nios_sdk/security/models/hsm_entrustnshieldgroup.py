# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmEntrustnshieldgroup - NIOS Entrust nShield HSM group.

All 13 properties from ``components.schemas.HsmEntrustnshieldgroup`` in the
v2.14 security swagger are represented here. Complex nested fields
``entrustnshield_hsm``, ``refresh_hsm``, and ``test_hsm_status`` are modelled
as ``dict[str, Any] | None`` - see NOTES.md.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "status",
        "uuid",
    }
)


class HsmEntrustnshieldgroup(BaseModel):
    """NIOS Entrust nShield HSM group.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    status: Literal["UP", "DOWN"] | str | None = Field(
        default=None, description="The status of all Entrust nShield HSM devices in the group."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    card_name: str | None = Field(
        default=None, description="The Entrust nShield HSM softcard name."
    )
    comment: str | None = Field(default=None, description="The Entrust nShield HSM group comment.")
    entrustnshield_hsm: list[dict[str, Any]] | None = Field(
        default=None, description="The list of Entrust nShield HSM devices."
    )
    key_server_ip: str | None = Field(
        default=None, description="The remote file server (RFS) IPv4 Address."
    )
    key_server_port: int | None = Field(
        default=None, description="The remote file server (RFS) port."
    )
    name: str | None = Field(default=None, description="The Entrust nShield HSM group name.")
    pass_phrase: str | None = Field(
        default=None,
        description="The password phrase used to unlock the Entrust nShield HSM keystore.",
    )
    protection: Literal["MODULE", "SOFTCARD"] | str | None = Field(
        default=None,
        description="The level of protection that the HSM group uses for the DNSSEC key data.",
    )
    refresh_hsm: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the refresh-HSM operation."
    )
    test_hsm_status: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the test-HSM-status operation."
    )
