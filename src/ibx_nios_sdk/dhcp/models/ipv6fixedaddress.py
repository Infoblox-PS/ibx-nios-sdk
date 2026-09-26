# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6fixedaddress - NIOS DHCP IPv6 fixed address.

All 54 properties from ``components.schemas.Ipv6fixedaddress`` in the v2.14 DHCP
swagger are represented here. Deeply nested types are inlined as dicts.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue, LogicFilterRule, MsDhcpOption

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "discover_now_status",
        "discovered_data",
        "ms_ad_user_data",
        "uuid",
    }
)


class Ipv6fixedaddress(BaseModel):
    """NIOS DHCP IPv6 fixed address."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    address_type: Literal["ADDRESS", "PREFIX", "BOTH"] | str | None = Field(
        default=None,
        description="The address type value for this IPv6 fixed address. When the address type is \"ADDRESS\", a value for the 'ipv6addr' member is required. When the address type is \"PREFIX\", values for 'ipv6prefix' and 'ipv6prefix_bits' are required. When the address type is \"BOTH\", values for 'ipv6addr', 'ipv6prefix', and 'ipv6prefix_bits' are all required.",
    )
    allow_telnet: bool | None = Field(
        default=None,
        description="This field controls whether the credential is used for both the Telnet and SSH credentials. If set to False, the credential is used only for SSH.",
    )
    always_update_dns: bool | None = Field(
        default=None,
        description="This field controls whether only the DHCPv6 server is allowed to update DNS, regardless of the DHCPv6 client requests.",
    )
    cli_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="The CLI credentials for the IPv6 fixed address."
    )
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )
    comment: str | None = Field(
        default=None, description="Comment for the fixed address; maximum 256 characters."
    )
    device_description: str | None = Field(
        default=None, description="The description of the device."
    )
    device_location: str | None = Field(default=None, description="The location of the device.")
    device_type: str | None = Field(default=None, description="The type of the device.")
    device_vendor: str | None = Field(default=None, description="The vendor of the device.")
    disable: bool | None = Field(
        default=None,
        description="Determines whether a fixed address is disabled or not. When this is set to False, the IPv6 fixed address is enabled.",
    )
    disable_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for this IPv6 fixed address is disabled or not. False means that the discovery is enabled.",
    )  # read-only
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(default=None, description="The discovery status of this IPv6 fixed address.")
    discovered_data: dict[str, Any] | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )
    domain_name: str | None = Field(
        default=None, description="The domain name for this IPv6 fixed address."
    )
    domain_name_servers: list[str] | None = Field(
        default=None,
        description="The IPv6 addresses of DNS recursive name servers to which the DHCP client can send name resolution requests. The DHCP server includes this information in the DNS Recursive Name Server option in Advertise, Rebind, Information-Request, and Reply messages.",
    )
    duid: str | None = Field(
        default=None, description="The DUID value for this IPv6 fixed address."
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP IPv6 fixed address object. If set to True, the DHCPv6 server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_immediate_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the IPv6 fixed address should be immediately enabled.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    ipv6addr: str | None = Field(
        default=None, description="The IPv6 Address of the DHCP IPv6 fixed address."
    )
    ipv6prefix: str | None = Field(
        default=None, description="The IPv6 Address prefix of the DHCP IPv6 fixed address."
    )
    ipv6prefix_bits: int | None = Field(
        default=None, description="Prefix bits of the DHCP IPv6 fixed address."
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied to this IPv6 fixed address. This list corresponds to the match rules that are written to the DHCPv6 configuration file.",
    )
    mac_address: str | None = Field(
        default=None, description="The MAC address for this IPv6 fixed address."
    )
    match_client: Literal["DUID", "MAC_ADDRESS"] | str | None = Field(
        default=None,
        description='The match_client value for this fixed address. Valid values are: "DUID": The fixed IP address is leased to the matching DUID. "MAC_ADDRESS": The fixed IP address is leased to the matching MAC address.',
    )
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )
    ms_iaid: int | None = Field(
        default=None, description="IAID associated with Microsoft IPv6 fixed address."
    )
    ms_options: list[MsDhcpOption] | None = Field(
        default=None,
        description="This field contains the Microsoft DHCPv6 options for this IPv6 fixed address.",
    )
    ms_server: dict[str, Any] | None = Field(
        default=None, description="The primary Microsoft Server."
    )
    name: str | None = Field(
        default=None, description="This field contains the name of this IPv6 fixed address."
    )
    network: str | None = Field(
        default=None,
        description="The network to which this IPv6 fixed address belongs, in IPv6 Address/CIDR format.",
    )
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which this IPv6 fixed address resides.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    preferred_lifetime: int | None = Field(
        default=None,
        description="The preferred lifetime value for this DHCP IPv6 fixed address object.",
    )
    reserved_interface: str | None = Field(
        default=None,
        description="The reference to the reserved interface to which the device belongs.",
    )
    restart_if_needed: bool | None = Field(
        default=None,
        description="Restarts the member service. The restart_if_needed flag can trigger a restart on DHCP services only when it is enabled on CP member.",
    )
    snmp3_credential: dict[str, Any] | None = Field(
        default=None, description="SNMPv3 credential used to manage this object."
    )
    snmp_credential: dict[str, Any] | None = Field(
        default=None, description="SNMP (v1/v2c) credential used to manage this object."
    )
    template: str | None = Field(
        default=None,
        description="If set on creation, the IPv6 fixed address will be created according to the values specified in the named template.",
    )
    use_cli_credentials: bool | None = Field(
        default=None,
        description="If set to true, the CLI credential will override member-level settings.",
    )
    use_domain_name: bool | None = Field(default=None, description="Use flag for: domain_name")
    use_domain_name_servers: bool | None = Field(
        default=None, description="Use flag for: domain_name_servers"
    )
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_ms_options: bool | None = Field(default=None, description="Use flag for: ms_options")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_snmp3_credential: bool | None = Field(
        default=None,
        description="Determines if the SNMPv3 credential should be used for the IPv6 fixed address.",
    )
    use_snmp_credential: bool | None = Field(
        default=None,
        description="If set to true, SNMP credential will override member level settings.",
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_lifetime: int | None = Field(
        default=None,
        description="The valid lifetime value for this DHCP IPv6 Fixed Address object.",
    )
