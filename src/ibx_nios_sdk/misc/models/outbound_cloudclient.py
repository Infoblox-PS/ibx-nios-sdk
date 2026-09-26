# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""OutboundCloudclient - NIOS outbound cloud client object.

Operations: GET collection, GET by ref, PUT (no POST/DELETE).

WAPI type: outbound:cloudclient

NOTES:
- 'uuid' is read-only.
- 'outbound_cloud_client_events' is a list of nested objects; typed as list[dict[str, Any]] | None.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class OutboundCloudclient(BaseModel):
    """NIOS outbound cloud client."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    enable: bool | None = Field(
        default=None, description="Determines whether the OutBound Cloud Client is enabled."
    )
    grid_member: str | None = Field(
        default=None, description="The Grid member where our outbound is running."
    )
    interval: int | None = Field(
        default=None,
        description="The time interval (in seconds) for requesting newly detected domains by the Infoblox Outbound Cloud Client and applying them to the list of configured RPZs.",
    )
    outbound_cloud_client_events: list[dict[str, Any]] | None = Field(
        default=None, description="List of event types to request"
    )
