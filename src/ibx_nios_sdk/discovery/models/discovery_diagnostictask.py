# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDiagnostictask - NIOS discovery diagnostic task.

Operations: GET (collection and by ref), PUT.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "start_time",
        "task_id",
        "uuid",
    }
)


class DiscoveryDiagnostictask(BaseModel):
    """NIOS discovery diagnostic task."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    start_time: int | None = Field(
        default=None, description="The time when the discovery diagnostic task was started."
    )
    task_id: str | None = Field(
        default=None, description="The ID of the discovery diagnostic task."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    community_string: str | None = Field(
        default=None, description="The SNMP community string of the discovery diagnostic task."
    )
    debug_snmp: bool | None = Field(
        default=None, description="The SNMP debug flag of the discovery diagnostic task."
    )
    force_test: bool | None = Field(
        default=None, description="The force test flag of the discovery diagnostic task."
    )
    ip_address: str | None = Field(
        default=None, description="The IP address of the discovery diagnostic task."
    )
    network_view: str | None = Field(
        default=None, description="The network view name of the discovery diagnostic task."
    )
