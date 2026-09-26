# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Multiregions - NIOS multi-regions object.

Operations: GET collection, GET by ref, PUT (no POST, no DELETE).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Multiregions(BaseModel):
    """NIOS multi-regions."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    cloud_platform: str | None = Field(
        default=None, description="Type of cloud_platform to get the supported regions."
    )
    govcloud_regions: str | None = Field(
        default=None,
        description="Comma separated sting containing only GovCloud supported regions.",
    )
    regions: str | None = Field(
        default=None, description="Comma separated string which contains all supported regions."
    )
