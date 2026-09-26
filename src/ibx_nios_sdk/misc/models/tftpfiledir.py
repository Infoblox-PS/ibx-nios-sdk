# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tftpfiledir - NIOS TFTP file directory object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: tftpfiledir

NOTES:
- 'is_synced_to_gm' and 'last_modify' are read-only.
- 'vtftp_dir_members' is a list of nested objects; typed as list[dict[str, Any]] | None.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "is_synced_to_gm",
        "last_modify",
    }
)


class Tftpfiledir(BaseModel):
    """NIOS TFTP file directory."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    is_synced_to_gm: bool | None = Field(
        default=None,
        description="Determines whether the TFTP entity is synchronized to Grid Master.",
    )
    last_modify: int | None = Field(
        default=None, description="The time when the file or directory was last modified."
    )  # --- writable ---
    directory: str | None = Field(
        default=None, description="The path to the directory that contains file or subdirectory."
    )
    name: str | None = Field(default=None, description="The TFTP directory or file name.")
    type: Literal["DIRECTORY", "FILE"] | str | None = Field(
        default=None, description="The type of TFTP file system entity (directory or file)."
    )
    vtftp_dir_members: list[dict[str, Any]] | None = Field(
        default=None,
        description="The replication members with TFTP client addresses where this virtual folder is applicable.",
    )
