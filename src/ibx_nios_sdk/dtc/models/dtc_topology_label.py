# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyLabel - NIOS DTC topology label.

Operations: GET only (collection and by ref). All non-_ref fields are read-only.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "field",
        "label",
    }
)


class DtcTopologyLabel(BaseModel):
    """NIOS DTC topology label - read-only."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    field: (
        Literal[
            "SUBNET", "CONTINENT", "COUNTRY", "SUBDIVISION", "CITY", "EA0", "EA1", "EA2", "EA3"
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The name of the field in the Topology database the label was obtained from.",
    )
    label: str | None = Field(default=None, description="The DTC Topology label name.")
