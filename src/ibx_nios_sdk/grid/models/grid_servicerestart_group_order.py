# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartGroupOrder - NIOS Grid service-restart group order."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset()


class GridServicerestartGroupOrder(BaseModel):
    """NIOS Grid service-restart group order."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    groups: list[str] | None = Field(
        default=None, description="The ordered list of the Service Restart Group."
    )
