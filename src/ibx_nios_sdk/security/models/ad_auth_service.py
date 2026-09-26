# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdAuthService - NIOS Active Directory authentication service.

All 9 properties from ``components.schemas.AdAuthService`` in the v2.14
security swagger are represented here. The ``domain_controllers`` field
is a list of nested domain controller objects, modelled as
``list[dict[str, Any]] | None`` - see NOTES.md.

WAPI type: ``ad_auth_service`` (underscore - verified via swagger path).

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class AdAuthService(BaseModel):
    """NIOS Active Directory authentication service.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    ad_domain: str | None = Field(
        default=None, description="The Active Directory domain to which this server belongs."
    )
    comment: str | None = Field(
        default=None, description="The descriptive comment for the AD authentication service."
    )
    disabled: bool | None = Field(
        default=None,
        description="Determines if Active Directory Authentication Service is disabled.",
    )
    domain_controllers: list[dict[str, Any]] | None = Field(
        default=None, description="The AD authentication server list."
    )
    name: str | None = Field(default=None, description="The AD authentication service name.")
    nested_group_querying: bool | None = Field(
        default=None, description="Determines whether the nested group querying is enabled."
    )
    timeout: int | None = Field(
        default=None,
        description="The number of seconds that the appliance waits for a response from the AD server.",
    )
