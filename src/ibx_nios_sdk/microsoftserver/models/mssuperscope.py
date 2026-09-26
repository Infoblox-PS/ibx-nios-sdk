# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Mssuperscope - NIOS MS server superscope.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "dhcp_utilization",
        "dhcp_utilization_status",
        "dynamic_hosts",
        "high_water_mark",
        "high_water_mark_reset",
        "low_water_mark",
        "low_water_mark_reset",
        "static_hosts",
        "total_hosts",
        "uuid",
    }
)


class Mssuperscope(BaseModel):
    """NIOS MS server superscope."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    dhcp_utilization: int | None = Field(
        default=None,
        description="The percentage of the total DHCP usage of the ranges in the superscope.",
    )
    dhcp_utilization_status: Literal["FULL", "HIGH", "LOW", "NORMAL"] | str | None = Field(
        default=None,
        description="Utilization level of the DHCP range objects that belong to the superscope.",
    )
    dynamic_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP leases issued for the DHCP range objects that belong to the superscope.",
    )
    static_hosts: int | None = Field(
        default=None,
        description="The number of static DHCP addresses configured in DHCP range objects that belong to the superscope.",
    )
    total_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP addresses configured in DHCP range objects that belong to the superscope.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(default=None, description="The superscope descriptive comment.")
    disable: bool | None = Field(
        default=None, description="Determines whether the superscope is disabled."
    )
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    high_water_mark: int | None = Field(
        default=None,
        description="The percentage value for DHCP range usage after which an alarm will be active.",
    )
    high_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage value for DHCP range usage after which an alarm will be reset.",
    )
    low_water_mark: int | None = Field(
        default=None,
        description="The percentage value for DHCP range usage below which an alarm will be active.",
    )
    low_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage value for DHCP range usage below which an alarm will be reset.",
    )
    name: str | None = Field(
        default=None, description="The name of the Microsoft DHCP superscope."
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which the superscope resides."
    )
    ranges: list[str] | None = Field(
        default=None,
        description="The list of DHCP ranges that are associated with the superscope.",
    )
