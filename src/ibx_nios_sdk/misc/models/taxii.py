# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Taxii - NIOS TAXII object.

Operations: GET collection, GET by ref, PUT (no POST/DELETE).

WAPI type: taxii

NOTES:
- 'uuid', 'ipv4addr', 'ipv6addr', 'name' are read-only.
- 'taxii_rpz_config' is a list of nested objects; typed as list[dict[str, Any]] | None.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "ipv4addr",
        "ipv6addr",
        "name",
        "uuid",
    }
)


class Taxii(BaseModel):
    """NIOS TAXII."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    ipv4addr: str | None = Field(default=None, description="The IPv4 Address of the Grid member.")
    ipv6addr: str | None = Field(default=None, description="The IPv6 Address of the Grid member.")
    name: str | None = Field(
        default=None, description="The name of the Taxii Member."
    )  # --- writable ---
    enable_service: bool | None = Field(
        default=None,
        description="Indicates whether the Taxii service is running on the given member or not.",
    )
    taxii_rpz_config: list[dict[str, Any]] | None = Field(
        default=None, description="Taxii service RPZ configuration list."
    )
