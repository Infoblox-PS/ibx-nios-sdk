# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6fixedaddresstemplate - NIOS DHCP IPv6 fixed address template.

All 19 properties from ``components.schemas.Ipv6fixedaddresstemplate`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue, LogicFilterRule

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Ipv6fixedaddresstemplate(BaseModel):
    """NIOS DHCP IPv6 fixed address template."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="A descriptive comment of an IPv6 fixed address template object."
    )
    domain_name: str | None = Field(
        default=None, description="Domain name of the IPv6 fixed address template object."
    )
    domain_name_servers: list[str] | None = Field(
        default=None,
        description="The IPv6 addresses of DNS recursive name servers to which the DHCP client can send name resolution requests. The DHCP server includes this information in the DNS Recursive Name Server option in Advertise, Rebind, Information-Request, and Reply messages.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied to this IPv6 fixed address. This list corresponds to the match rules that are written to the DHCPv6 configuration file.",
    )
    name: str | None = Field(
        default=None, description="Name of an IPv6 fixed address template object."
    )
    number_of_addresses: int | None = Field(
        default=None, description="The number of IPv6 addresses for this fixed address."
    )
    offset: int | None = Field(
        default=None, description="The start address offset for this IPv6 fixed address."
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    preferred_lifetime: int | None = Field(
        default=None,
        description="The preferred lifetime value for this DHCP IPv6 fixed address template object.",
    )
    use_domain_name: bool | None = Field(default=None, description="Use flag for: domain_name")
    use_domain_name_servers: bool | None = Field(
        default=None, description="Use flag for: domain_name_servers"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_lifetime: int | None = Field(
        default=None,
        description="The valid lifetime value for this DHCP IPv6 fixed address template object.",
    )
