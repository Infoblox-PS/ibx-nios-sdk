# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Filternac - NIOS DHCP NAC filter."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Filternac(BaseModel):
    """NIOS DHCP NAC filter."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="The descriptive comment of a DHCP NAC Filter object."
    )
    expression: str | None = Field(
        default=None, description="The conditional expression of a DHCP NAC Filter object."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    lease_time: int | None = Field(
        default=None,
        description="The length of time the DHCP server leases an IP address to a client. The lease time applies to hosts that meet the filter criteria.",
    )
    name: str | None = Field(default=None, description="The name of a DHCP NAC Filter object.")
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
