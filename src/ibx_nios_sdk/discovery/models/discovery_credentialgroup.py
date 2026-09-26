# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryCredentialgroup - NIOS discovery credential group.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class DiscoveryCredentialgroup(BaseModel):
    """NIOS discovery credential group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable ---
    name: str | None = Field(default=None, description="The name of the Credential group.")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
