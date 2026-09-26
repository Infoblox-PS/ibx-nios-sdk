# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SamlAuthservice - NIOS SAML authentication service.

All 6 properties from ``components.schemas.SamlAuthservice`` in the v2.14
security swagger are represented here. The ``idp`` field is a nested identity
provider object, modelled as ``dict[str, Any] | None`` - see NOTES.md.

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


class SamlAuthservice(BaseModel):
    """NIOS SAML authentication service.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The descriptive comment for the SAML authentication service."
    )
    idp: dict[str, Any] | None = Field(default=None)
    name: str | None = Field(
        default=None, description="The name of the SAML authentication service."
    )
    session_timeout: int | None = Field(
        default=None, description="The session timeout in seconds."
    )
