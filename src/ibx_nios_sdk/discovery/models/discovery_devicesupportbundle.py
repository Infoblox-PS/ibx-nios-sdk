# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDevicesupportbundle - NIOS discovery device support bundle.

Operations: GET (collection and by ref), DELETE.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "author",
        "integrated_ind",
        "name",
        "version",
    }
)


class DiscoveryDevicesupportbundle(BaseModel):
    """NIOS discovery device support bundle."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    author: str | None = Field(
        default=None, description="The developer of the device support bundle."
    )
    integrated_ind: bool | None = Field(
        default=None,
        description="Determines whether the device support bundle is integrated or imported. Note that integrated support bundles cannot be removed.",
    )
    version: str | None = Field(
        default=None, description="The version of the currently active device support bundle."
    )  # --- writable ---
    name: str | None = Field(
        default=None, description="The descriptive device name for the device support bundle."
    )
