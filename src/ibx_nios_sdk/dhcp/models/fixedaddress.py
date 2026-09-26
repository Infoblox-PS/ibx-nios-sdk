# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Fixedaddress - NIOS DHCP IPv4 fixed address.

All 62 properties from ``components.schemas.Fixedaddress`` in the v2.14 DHCP
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
        "is_invalid_mac",
        "ms_ad_user_data",
        "uuid",
    }
)


class Fixedaddress(BaseModel):
    """NIOS DHCP IPv4 fixed address."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    agent_circuit_id: str | None = Field(
        default=None, description="The agent circuit ID for the fixed address."
    )
    agent_remote_id: str | None = Field(
        default=None, description="The agent remote ID for the fixed address."
    )
    allow_telnet: bool | None = Field(
        default=None,
        description="This field controls whether the credential is used for both the Telnet and SSH credentials. If set to False, the credential is used only for SSH.",
    )
    always_update_dns: bool | None = Field(
        default=None,
        description="This field controls whether only the DHCP server is allowed to update DNS, regardless of the DHCP client requests.",
    )
    bootfile: str | None = Field(
        default=None,
        description="The bootfile name for the fixed address. You can configure the DHCP server to support clients that use the boot file name option in their DHCPREQUEST messages.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The bootserver address for the fixed address. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
    )
    cli_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="The CLI credentials for the fixed address."
    )
    client_identifier_prepend_zero: bool | None = Field(
        default=None,
        description="This field controls whether there is a prepend for the dhcp-client-identifier of a fixed address.",
    )
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )
    comment: str | None = Field(
        default=None, description="Comment for the fixed address; maximum 256 characters."
    )
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this fixed address.",
    )
    ddns_hostname: str | None = Field(
        default=None, description="The DDNS host name for this fixed address."
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="If set to true, BOOTP settings are disabled and BOOTP requests will be denied.",
    )
    device_description: str | None = Field(
        default=None, description="The description of the device."
    )
    device_location: str | None = Field(default=None, description="The location of the device.")
    device_type: str | None = Field(default=None, description="The type of the device.")
    device_vendor: str | None = Field(default=None, description="The vendor of the device.")
    dhcp_client_identifier: str | None = Field(
        default=None, description="The DHCP client ID for the fixed address."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a fixed address is disabled or not. When this is set to False, the fixed address is enabled.",
    )
    disable_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for this fixed address is disabled or not. False means that the discovery is enabled.",
    )  # read-only
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(default=None, description="The discovery status of this fixed address.")
    discovered_data: dict[str, Any] | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP Fixed Address object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_immediate_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the fixed address should be immediately enabled.",
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="If this field is set to False, the appliance returns all DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )
    ipv4addr: str | None = Field(
        default=None, description="The IPv4 Address of the fixed address."
    )  # read-only
    is_invalid_mac: bool | None = Field(
        default=None,
        description="This flag reflects whether the MAC address for this fixed address is invalid.",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the this fixed address. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )
    mac: str | None = Field(
        default=None, description="The MAC address value for this fixed address."
    )
    match_client: (
        Literal["MAC_ADDRESS", "CLIENT_ID", "RESERVED", "CIRCUIT_ID", "REMOTE_ID"] | str | None
    ) = Field(
        default=None,
        description='The match_client value for this fixed address. Valid values are: "MAC_ADDRESS": The fixed IP address is leased to the matching MAC address. "CLIENT_ID": The fixed IP address is leased to the matching DHCP client identifier. "RESERVED": The fixed IP address is reserved for later use with a MAC address that only has zeros. "CIRCUIT_ID": The fixed IP address is leased to the DHCP client with a matching circuit ID. Note that the "agent_circuit_id" field must be set in this case. "REMOTE_ID": The fixed IP address is leased to the DHCP client with a matching remote ID. Note that the "agent_remote_id" field must be set in this case.',
    )
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )
    ms_options: list[MsDhcpOption] | None = Field(
        default=None,
        description="This field contains the Microsoft DHCP options for this fixed address.",
    )
    ms_server: dict[str, Any] | None = Field(
        default=None, description="The primary Microsoft Server."
    )
    name: str | None = Field(
        default=None, description="This field contains the name of this fixed address."
    )
    network: str | None = Field(
        default=None,
        description="The network to which this fixed address belongs, in IPv4 Address/CIDR format.",
    )
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which this fixed address resides.",
    )
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address format of the next server that the host needs to boot.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value for a DHCP Fixed Address object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    reserved_interface: str | None = Field(
        default=None, description="The ref to the reserved interface to which the device belongs."
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
        description="If set on creation, the fixed address will be created according to the values specified in the named template.",
    )
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_cli_credentials: bool | None = Field(
        default=None,
        description="If set to true, the CLI credential will override member-level settings.",
    )
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_deny_bootp: bool | None = Field(default=None, description="Use flag for: deny_bootp")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_ms_options: bool | None = Field(default=None, description="Use flag for: ms_options")
    use_nextserver: bool | None = Field(default=None, description="Use flag for: nextserver")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_pxe_lease_time: bool | None = Field(
        default=None, description="Use flag for: pxe_lease_time"
    )
    use_snmp3_credential: bool | None = Field(
        default=None,
        description="Determines if the SNMPv3 credential should be used for the fixed address.",
    )
    use_snmp_credential: bool | None = Field(
        default=None,
        description="If set to true, the SNMP credential will override member-level settings.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
