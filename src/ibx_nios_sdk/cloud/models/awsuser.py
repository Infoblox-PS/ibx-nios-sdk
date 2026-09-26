# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Awsuser - NIOS AWS user object.

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


class Awsuser(BaseModel):
    """NIOS AWS user."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    status: Literal["UNUSED", "SUCCESSFUL", "UNSUCCESSFUL"] | str | None = Field(
        default=None, description="Indicate the validity status of this AWS user."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    access_key_id: str | None = Field(
        default=None,
        description="The unique Access Key ID of this AWS user. Maximum 255 characters.",
    )
    account_id: str | None = Field(
        default=None, description="The AWS Account ID of this AWS user. Maximum 64 characters."
    )
    govcloud_enabled: bool | None = Field(
        default=None, description="Indicates if gov cloud is enabled or disabled."
    )
    name: str | None = Field(default=None, description="The AWS user name. Maximum 64 characters.")
    nios_user_name: str | None = Field(
        default=None,
        description="The NIOS user name mapped to this AWS user. Maximum 64 characters.",
    )
    last_used: int | None = Field(
        default=None, description="The timestamp when this AWS user credentials was last used."
    )
    secret_access_key: str | None = Field(
        default=None,
        description="The Secret Access Key for the Access Key ID of this user. Maximum 255 characters.",
    )
