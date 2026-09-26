# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RadiusAuthservice - NIOS RADIUS authentication service.

All 15 properties from ``components.schemas.RadiusAuthservice`` in the v2.14
security swagger are represented here. Complex nested fields
``check_radius_server_settings`` and ``servers`` are modelled as
``dict[str, Any] | None`` / ``list[dict[str, Any]] | None`` - see NOTES.md.

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
        "uuid",
    }
)


class RadiusAuthservice(BaseModel):
    """NIOS RADIUS authentication service.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    acct_retries: int | None = Field(
        default=None,
        description="The number of times to attempt to contact an accounting RADIUS server.",
    )
    acct_timeout: int | None = Field(
        default=None,
        description="The number of seconds to wait for a response from the RADIUS server.",
    )
    auth_retries: int | None = Field(
        default=None,
        description="The number of times to attempt to contact an authentication RADIUS server.",
    )
    auth_timeout: int | None = Field(
        default=None,
        description="The number of seconds to wait for a response from the RADIUS server.",
    )
    cache_ttl: int | None = Field(
        default=None, description="The TTL of cached authentication data in seconds."
    )
    check_radius_server_settings: dict[str, Any] | None = Field(default=None)
    comment: str | None = Field(default=None, description="The RADIUS descriptive comment.")
    disable: bool | None = Field(
        default=None,
        description="Determines whether the RADIUS authentication service is disabled.",
    )
    enable_cache: bool | None = Field(
        default=None, description="Determines whether the authentication cache is enabled."
    )
    mode: Literal["HUNT_GROUP", "ROUND_ROBIN"] | str | None = Field(
        default=None, description="The way to contact the RADIUS server."
    )
    name: str | None = Field(default=None, description="The RADIUS authentication service name.")
    recovery_interval: int | None = Field(
        default=None,
        description="The time period to wait before retrying a server that has been marked as down.",
    )
    servers: list[dict[str, Any]] | None = Field(
        default=None, description="The ordered list of RADIUS authentication servers."
    )
