# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcPool - NIOS DTC pool object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

Complex fields lb_dynamic_ratio_alternate and lb_dynamic_ratio_preferred
reference nested schemas - modelled as dict[str, Any] | None. See NOTES.md.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "health",
        "uuid",
    }
)


class DtcPool(BaseModel):
    """NIOS DTC pool."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    auto_consolidated_monitors: bool | None = Field(
        default=None,
        description="Flag for enabling auto managing DTC Consolidated Monitors in DTC Pool.",
    )
    availability: Literal["ALL", "ANY", "QUORUM"] | str | None = Field(
        default=None,
        description="A resource in the pool is available if ANY, at least QUORUM, or ALL monitors for the pool say that it is up.",
    )
    comment: str | None = Field(
        default=None, description="The comment for the DTC Pool; maximum 256 characters."
    )
    consolidated_monitors: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of monitors and associated members statuses of which are shared across members and consolidated in server availability determination.",
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether the DTC Pool is disabled or not. When this is set to False, the fixed address is enabled.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    health: dict[str, Any] | None = Field(default=None, description="Health status of the object.")
    lb_alternate_method: (
        Literal[
            "ALL_AVAILABLE",
            "DYNAMIC_RATIO",
            "GLOBAL_AVAILABILITY",
            "NONE",
            "RATIO",
            "ROUND_ROBIN",
            "SOURCE_IP_HASH",
            "TOPOLOGY",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The alternate load balancing method. Use this to select a method type from the pool if the preferred method does not return any results.",
    )
    lb_alternate_topology: str | None = Field(
        default=None, description="The alternate topology for load balancing."
    )
    lb_dynamic_ratio_alternate: dict[str, Any] | None = Field(default=None)
    lb_dynamic_ratio_preferred: dict[str, Any] | None = Field(default=None)
    lb_preferred_method: (
        Literal[
            "ALL_AVAILABLE",
            "DYNAMIC_RATIO",
            "GLOBAL_AVAILABILITY",
            "RATIO",
            "ROUND_ROBIN",
            "SOURCE_IP_HASH",
            "TOPOLOGY",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The preferred load balancing method. Use this to select a method type from the pool.",
    )
    lb_preferred_topology: str | None = Field(
        default=None, description="The preferred topology for load balancing."
    )
    monitors: list[str | dict[str, Any]] | None = Field(
        default=None,
        description="The monitors related to pool. WAPI accepts (and returns) bare ref strings.",
    )
    name: str | None = Field(default=None, description="The DTC Pool display name.")
    quorum: int | None = Field(
        default=None,
        description="For availability mode QUORUM, at least this many monitors must report the resource as up for it to be available",
    )
    servers: list[dict[str, Any]] | None = Field(
        default=None, description="The servers related to the pool."
    )
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for the DTC Pool. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
    )
    use_ttl: bool | None = Field(default=None, description="Use flag for: ttl")
