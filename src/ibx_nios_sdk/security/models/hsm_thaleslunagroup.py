# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmThaleslunagroup - NIOS Thales Luna HSM group.

All 11 properties from ``components.schemas.HsmThaleslunagroup`` in the v2.14
security swagger are represented here. Complex nested fields ``thalesluna``,
``refresh_hsm``, and ``test_hsm_status`` are modelled as
``dict[str, Any] | None`` - see NOTES.md.

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
        "group_sn",
        "status",
        "uuid",
    }
)


class HsmThaleslunagroup(BaseModel):
    """NIOS Thales Luna HSM group.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    group_sn: str | None = Field(
        default=None, description="The HSM Thales Luna group serial number."
    )
    status: Literal["UP", "DOWN"] | str | None = Field(
        default=None, description="The status of all HSM Thales Luna devices in the group."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(default=None, description="The HSM Thales Luna group comment.")
    hsm_version: Literal["Luna_4", "Luna_5", "Luna_6", "Luna_7_CPL"] | str | None = Field(
        default=None, description="The HSM Thales Luna version."
    )
    name: str | None = Field(default=None, description="The HSM Thales Luna group name.")
    pass_phrase: str | None = Field(
        default=None, description="The pass phrase used to unlock the HSM Thales Luna keystore."
    )
    refresh_hsm: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the refresh-HSM operation."
    )
    test_hsm_status: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the test-HSM-status operation."
    )
    thalesluna: list[dict[str, Any]] | None = Field(
        default=None, description="The list of HSM Thales Luna devices."
    )
