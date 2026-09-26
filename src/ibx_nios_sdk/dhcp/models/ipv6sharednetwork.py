# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6sharednetwork - NIOS DHCP IPv6 shared network.

All 33 properties from ``components.schemas.Ipv6sharednetwork`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from typing import Any

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


class Ipv6sharednetwork(BaseModel):
    """NIOS DHCP IPv6 shared network."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="Comment for the IPv6 shared network, maximum 256 characters."
    )
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this network.",
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="This field controls whether only the DHCP server is allowed to update DNS, regardless of the DHCP clients requests. Note that changes for this field take effect only if ddns_use_option81 is True.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DNS update Time to Live (TTL) value of an IPv6 shared network object. The TTL is a 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    ddns_use_option81: bool | None = Field(
        default=None,
        description="The support for DHCP Option 81 at the IPv6 shared network level.",
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether an IPv6 shared network is disabled or not. When this is set to False, the IPv6 shared network is enabled.",
    )
    domain_name: str | None = Field(
        default=None,
        description="Use this method to set or retrieve the domain_name value of a DHCP IPv6 Shared Network object.",
    )
    domain_name_servers: list[str] | None = Field(
        default=None,
        description="Use this method to set or retrieve the dynamic DNS updates flag of a DHCP IPv6 Shared Network object. The DHCP server can send DDNS updates to DNS servers in the same Grid and to external DNS servers. This setting overrides the member level settings.",
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of an IPv6 shared network object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the this IPv6 shared network. This list corresponds to the match rules that are written to the DHCPv6 configuration file.",
    )
    name: str | None = Field(default=None, description="The name of the IPv6 Shared Network.")
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which this IPv6 shared network resides.",
    )
    networks: list[Any] | None = Field(
        default=None,
        description="A list of IPv6 networks belonging to the shared network Each individual list item must be specified as an object containing a '_ref' parameter to a network reference, for example:: [{ \"_ref\": \"ipv6network/ZG5zdHdvcmskMTAuAvMTYvMA\", }] if the reference of the wanted network is not known, it is possible to specify search parameters for the network instead in the following way:: [{ \"_ref\": { 'network': 'aabb::/64', } }] note that in this case the search must match exactly one network for the assignment to be successful.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    preferred_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the preferred lifetime value of a DHCP IPv6 Shared Network object.",
    )
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_ddns_generate_hostname: bool | None = Field(
        default=None, description="Use flag for: ddns_generate_hostname"
    )
    use_ddns_ttl: bool | None = Field(default=None, description="Use flag for: ddns_ttl")
    use_ddns_use_option81: bool | None = Field(
        default=None, description="Use flag for: ddns_use_option81"
    )
    use_domain_name: bool | None = Field(default=None, description="Use flag for: domain_name")
    use_domain_name_servers: bool | None = Field(
        default=None, description="Use flag for: domain_name_servers"
    )
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_update_dns_on_lease_renewal: bool | None = Field(
        default=None, description="Use flag for: update_dns_on_lease_renewal"
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the valid lifetime value of a DHCP IPv6 Shared Network object.",
    )
