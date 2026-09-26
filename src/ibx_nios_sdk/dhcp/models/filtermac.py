# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Filtermac - NIOS DHCP MAC filter."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Filtermac(BaseModel):
    """NIOS DHCP MAC filter."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="The descriptive comment of a DHCP MAC Filter object."
    )
    default_mac_address_expiration: int | None = Field(
        default=None,
        description="The default MAC expiration time of the DHCP MAC Address Filter object. By default, the MAC address filter never expires; otherwise, it is the absolute interval when the MAC address filter expires. The maximum value can extend up to 4294967295 secs. The minimum value is 60 secs (1 min).",
    )
    disable: bool | None = Field(
        default=None, description="Determines if the DHCP Fingerprint object is disabled or not."
    )
    enforce_expiration_times: bool | None = Field(
        default=None,
        description="The flag to enforce MAC address expiration of the DHCP MAC Address Filter object.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    lease_time: int | None = Field(
        default=None,
        description="The length of time the DHCP server leases an IP address to a client. The lease time applies to hosts that meet the filter criteria.",
    )
    name: str | None = Field(default=None, description="The name of a DHCP MAC Filter object.")
    never_expires: bool | None = Field(
        default=None,
        description="Determines if DHCP MAC Filter never expires or automatically expires.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    reserved_for_infoblox: str | None = Field(
        default=None,
        description="This is reserved for writing comments related to the particular MAC address filter. The length of comment cannot exceed 1024 bytes.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
