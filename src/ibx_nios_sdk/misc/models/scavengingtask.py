# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Scavengingtask - NIOS scavenging task (read-only).

Operations: GET collection, GET by ref (read-only, no POST/PUT/DELETE).

WAPI type: scavengingtask

NOTES:
- All fields are read-only.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "action",
        "associated_object",
        "end_time",
        "processed_records",
        "reclaimable_records",
        "reclaimed_records",
        "start_time",
        "status",
        "uuid",
    }
)


class Scavengingtask(BaseModel):
    """NIOS scavenging task."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    action: Literal["ANALYZE", "RECLAIM", "ANALYZE_RECLAIM", "RESET"] | str | None = Field(
        default=None, description="The scavenging action."
    )
    associated_object: str | None = Field(
        default=None,
        description="The reference to the object associated with the scavenging task.",
    )
    end_time: int | None = Field(default=None, description="The scavenging process end time.")
    processed_records: int | None = Field(
        default=None, description="The number of processed during scavenging resource records."
    )
    reclaimable_records: int | None = Field(
        default=None,
        description="The number of resource records that are allowed to be reclaimed during the scavenging process.",
    )
    reclaimed_records: int | None = Field(
        default=None,
        description="The number of reclaimed during the scavenging process resource records.",
    )
    start_time: int | None = Field(default=None, description="The scavenging process start time.")
    status: Literal["CREATED", "RUNNING", "COMPLETED", "ERROR"] | str | None = Field(
        default=None, description="The scavenging process status. This is a read-only attribute."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
