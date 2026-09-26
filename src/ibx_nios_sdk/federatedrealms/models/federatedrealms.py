# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Federatedrealms - NIOS federated realm object.

Operations: GET collection, GET by ref (read-only - no POST, PUT, DELETE).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "id",
        "name",
    }
)


class Federatedrealms(BaseModel):
    """NIOS federated realm."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    id: str | None = Field(default=None, description="Federated realm id.")
    name: str | None = Field(default=None, description="Federated realm name.")
