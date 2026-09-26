# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Roaminghost - NIOS DHCP roaming host.

All 55 properties from ``components.schemas.Roaminghost`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "ipv6_client_hostname",
        "uuid",
    }
)


class Roaminghost(BaseModel):
    """NIOS DHCP roaming host."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    address_type: Literal["IPV4", "IPV6", "BOTH"] | str | None = Field(
        default=None, description="The address type for this roaming host."
    )
    bootfile: str | None = Field(
        default=None,
        description="The bootfile name for the roaming host. You can configure the DHCP server to support clients that use the boot file name option in their DHCPREQUEST messages.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The boot server address for the roaming host. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
    )
    client_identifier_prepend_zero: bool | None = Field(
        default=None,
        description="This field controls whether there is a prepend for the dhcp-client-identifier of a roaming host.",
    )
    comment: str | None = Field(
        default=None, description="Comment for the roaming host; maximum 256 characters."
    )
    ddns_domainname: str | None = Field(
        default=None, description="The DDNS domain name for this roaming host."
    )
    ddns_hostname: str | None = Field(
        default=None, description="The DDNS host name for this roaming host."
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="If set to true, BOOTP settings are disabled and BOOTP requests will be denied.",
    )
    dhcp_client_identifier: str | None = Field(
        default=None, description="The DHCP client ID for the roaming host."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a roaming host is disabled or not. When this is set to False, the roaming host is enabled.",
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of the roaming host object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    force_roaming_hostname: bool | None = Field(
        default=None,
        description="Set this to True to use the roaming host name as its ddns_hostname.",
    )
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="If this field is set to False, the appliance returns all the DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )  # read-only
    ipv6_client_hostname: str | None = Field(
        default=None,
        description="The client hostname of a DHCP roaming host object. This field specifies the host name that the DHCP client sends to the Infoblox appliance using DHCP option 12.",
    )
    ipv6_ddns_domainname: str | None = Field(
        default=None, description="The IPv6 DDNS domain name for this roaming host."
    )
    ipv6_ddns_hostname: str | None = Field(
        default=None, description="The IPv6 DDNS host name for this roaming host."
    )
    ipv6_domain_name: str | None = Field(
        default=None, description="The IPv6 domain name for this roaming host."
    )
    ipv6_domain_name_servers: list[str] | None = Field(
        default=None,
        description="The IPv6 addresses of DNS recursive name servers to which the DHCP client can send name resolution requests. The DHCP server includes this information in the DNS Recursive Name Server option in Advertise, Rebind, Information-Request, and Reply messages.",
    )
    ipv6_duid: str | None = Field(
        default=None, description="The DUID value for this roaming host."
    )
    ipv6_enable_ddns: bool | None = Field(
        default=None, description="Set this to True to enable IPv6 DDNS."
    )
    ipv6_force_roaming_hostname: bool | None = Field(
        default=None,
        description="Set this to True to use the roaming host name as its ddns_hostname.",
    )
    ipv6_mac_address: str | None = Field(
        default=None, description="The MAC address for this roaming host."
    )
    ipv6_match_option: Literal["DUID", "V6_MAC_ADDRESS"] | str | None = Field(
        default=None,
        description='The identification method for an IPv6 or mixed IPv4/IPv6 roaming host. The supported values for this field are "DUID" or "V6_MAC_ADDRESS", which specify what option should be used to identify the specific DHCPv6 client.',
    )
    ipv6_options: list[dict[str, Any]] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    ipv6_template: str | None = Field(
        default=None,
        description="If set on creation, the roaming host will be created according to the values specified in the named IPv6 roaming host template.",
    )
    mac: str | None = Field(default=None, description="The MAC address for this roaming host.")
    match_client: Literal["MAC_ADDRESS", "CLIENT_ID"] | str | None = Field(
        default=None,
        description='The match-client value for this roaming host. Valid values are: "MAC_ADDRESS": The fixed IP address is leased to the matching MAC address. "CLIENT_ID": The fixed IP address is leased to the matching DHCP client identifier.',
    )
    name: str | None = Field(default=None, description="The name of this roaming host.")
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which this roaming host resides.",
    )
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address format of the next server that the host needs to boot.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    preferred_lifetime: int | None = Field(
        default=None, description="The preferred lifetime value for this roaming host object."
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value for this roaming host object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    template: str | None = Field(
        default=None,
        description="If set on creation, the roaming host will be created according to the values specified in the named template.",
    )
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_deny_bootp: bool | None = Field(default=None, description="Use flag for: deny_bootp")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_ipv6_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ipv6_ddns_domainname"
    )
    use_ipv6_domain_name: bool | None = Field(
        default=None, description="Use flag for: ipv6_domain_name"
    )
    use_ipv6_domain_name_servers: bool | None = Field(
        default=None, description="Use flag for: ipv6_domain_name_servers"
    )
    use_ipv6_enable_ddns: bool | None = Field(
        default=None, description="Use flag for: ipv6_enable_ddns"
    )
    use_ipv6_options: bool | None = Field(default=None, description="Use flag for: ipv6_options")
    use_nextserver: bool | None = Field(default=None, description="Use flag for: nextserver")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_pxe_lease_time: bool | None = Field(
        default=None, description="Use flag for: pxe_lease_time"
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_lifetime: int | None = Field(
        default=None, description="The valid lifetime value for this roaming host object."
    )
