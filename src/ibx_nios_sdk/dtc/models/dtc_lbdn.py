# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcLbdn - NIOS DTC LBDN (Load-Balanced Domain Name) object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

``pools`` is an array of pool-priority structs - modelled as
``list[dict[str, Any]] | None``. See NOTES.md.
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


class DtcLbdn(BaseModel):
    """NIOS DTC LBDN."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    auth_zones: list[str] | None = Field(default=None, description="List of linked auth zones.")
    auto_consolidated_monitors: bool | None = Field(
        default=None,
        description="Flag for enabling auto managing DTC Consolidated Monitors on related DTC Pools.",
    )
    comment: str | None = Field(
        default=None, description="Comment for the DTC LBDN; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether the DTC LBDN is disabled or not. When this is set to False, the fixed address is enabled.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    health: dict[str, Any] | None = Field(default=None, description="Health status of the object.")
    lb_method: (
        Literal["GLOBAL_AVAILABILITY", "RATIO", "ROUND_ROBIN", "SOURCE_IP_HASH", "TOPOLOGY"]
        | str
        | None
    ) = Field(default=None, description="The load balancing method. Used to select pool.")
    name: str | None = Field(
        default=None, description="The display name of the DTC LBDN, not DNS related."
    )
    patterns: list[str] | None = Field(
        default=None, description="LBDN wildcards for pattern match."
    )
    persistence: int | None = Field(
        default=None,
        description="Maximum time, in seconds, for which client specific LBDN responses will be cached. Zero specifies no caching.",
    )
    pools: list[dict[str, Any]] | None = Field(default=None, description="Pools linked to LBDN.")
    priority: int | None = Field(
        default=None,
        description='The LBDN pattern match priority for "overlapping" DTC LBDN objects. LBDNs are "overlapping" if they are simultaneously assigned to a zone and have patterns that can match the same FQDN. The matching LBDN with highest priority (lowest ordinal) will be used.',
    )
    topology: str | None = Field(
        default=None, description="The topology rules for TOPOLOGY method."
    )
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for the DTC LBDN. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
    )
    types: list[Literal["A", "AAAA", "NAPTR", "CNAME", "SRV"] | str] | None = Field(
        default=None, description="The list of resource record types supported by LBDN."
    )
    use_ttl: bool | None = Field(default=None, description="Use flag for: ttl")
