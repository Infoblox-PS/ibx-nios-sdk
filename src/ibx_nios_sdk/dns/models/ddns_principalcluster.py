# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DdnsPrincipalcluster - NIOS DDNS principal cluster.

All 6 properties from ``components.schemas.DdnsPrincipalcluster`` in the
v2.14 DNS swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main DdnsPrincipalcluster model
# ---------------------------------------------------------------------------


class DdnsPrincipalcluster(BaseModel):
    """NIOS DDNS principal cluster."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable fields ---
    name: str | None = Field(default=None, description="The name of this DDNS Principal Cluster.")
    comment: str | None = Field(
        default=None, description="Comment for the DDNS Principal Cluster."
    )
    group: str | None = Field(default=None, description="The DDNS Principal cluster group name.")
    principals: list[str] | None = Field(
        default=None, description="The list of equivalent principals."
    )  # --- read-only fields ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO
