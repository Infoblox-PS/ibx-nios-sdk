# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Allendpoints - NIOS allendpoints read-only aggregate object.

Operations: GET collection, GET by ref (read-only, no POST/PUT/DELETE).

WAPI type: allendpoints

NOTES:
- All fields except _ref are read-only.
- This is an aggregate view of all endpoint objects.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "comment",
        "disable",
        "subscribing_member",
        "type",
        "version",
    }
)


class Allendpoints(BaseModel):
    """NIOS allendpoints aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    address: str | None = Field(
        default=None,
        description="The Grid endpoint IPv4 Address or IPv6 Address or Fully-Qualified Domain Name (FQDN).",
    )
    comment: str | None = Field(default=None, description="The Grid endpoint descriptive comment.")
    disable: bool | None = Field(
        default=None,
        description="Determines whether a Grid endpoint is disabled or not. When this is set to False, the Grid endpoint is enabled.",
    )
    subscribing_member: str | None = Field(
        default=None,
        description="The name of the Grid Member object that is serving Grid endpoint.",
    )
    type: Literal["TYPE_CISCO", "TYPE_RESTAPI", "TYPE_DXL"] | str | None = Field(
        default=None, description="The Grid endpoint type."
    )
    version: str | None = Field(default=None, description="The Grid endpoint version.")
