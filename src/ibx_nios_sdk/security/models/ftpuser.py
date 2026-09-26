# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ftpuser - NIOS FTP user.

All 8 properties from ``components.schemas.Ftpuser`` in the v2.14 security
swagger are represented here.

Note: The primary identifier field is ``username`` (not ``name``). See NOTES.md
for the discrepancy from the plan.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Ftpuser(BaseModel):
    """NIOS FTP user.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.

    Note: primary identifier is ``username`` (not ``name``).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    create_home_dir: bool | None = Field(
        default=None,
        description="Determines whether to create the home directory with the user name or to use the existing directory as the home directory.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    home_dir: str | None = Field(
        default=None, description="The absolute path of the FTP user's home directory."
    )
    password: str | None = Field(default=None, description="The FTP user password.")
    permission: Literal["RO", "RW"] | str | None = Field(
        default=None, description="The FTP user permission."
    )
    username: str | None = Field(default=None, description="The FTP user name.")
