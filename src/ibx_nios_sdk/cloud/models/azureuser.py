# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Azureuser - NIOS Azure user object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "status",
        "uuid",
    }
)


class Azureuser(BaseModel):
    """NIOS Azure user."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    status: Literal["UNUSED", "SUCCESSFUL", "UNSUCCESSFUL"] | str | None = Field(
        default=None, description="Indicate the validity status of this Azure user."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    client_id: str | None = Field(
        default=None,
        description="The unique Client ID of this Azure user. Maximum 255 characters.",
    )
    name: str | None = Field(
        default=None, description="The Azure user name. Maximum 64 characters."
    )
    tenant_id: str | None = Field(
        default=None, description="The Azure Tenant ID of this Azure user. Maximum 64 characters."
    )
    client_secret_key: str | None = Field(
        default=None,
        description="The Client Secret Key for the Client ID of this user. Maximum 255 characters.",
    )
    last_used: int | None = Field(
        default=None, description="The timestamp when this Azure user credentials was last used."
    )
