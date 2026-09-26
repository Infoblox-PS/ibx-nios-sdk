# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""TacacsplusAuthservice - NIOS TACACS+ authentication service.

All 11 properties from ``components.schemas.TacacsplusAuthservice`` in the
v2.14 security swagger are represented here. Complex nested fields
``check_tacacsplus_server_settings`` and ``servers`` are modelled as
``dict[str, Any] | None`` / ``list[dict[str, Any]] | None`` - see NOTES.md.

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


class TacacsplusAuthservice(BaseModel):
    """NIOS TACACS+ authentication service.

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
        description="The number of the accounting retries before giving up and moving on to the next server.",
    )
    acct_timeout: int | None = Field(
        default=None, description="The accounting retry period in milliseconds."
    )
    auth_retries: int | None = Field(
        default=None,
        description="The number of the authentication/authorization retries before giving up and moving on to the next server.",
    )
    auth_timeout: int | None = Field(
        default=None,
        description="The authentication/authorization timeout period in milliseconds.",
    )
    check_tacacsplus_server_settings: dict[str, Any] | None = Field(default=None)
    comment: str | None = Field(
        default=None, description="The TACACS+ authentication service descriptive comment."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether the TACACS+ authentication service object is disabled.",
    )
    name: str | None = Field(default=None, description="The TACACS+ authentication service name.")
    servers: list[dict[str, Any]] | None = Field(
        default=None, description="The list of the TACACS+ servers used for authentication."
    )
