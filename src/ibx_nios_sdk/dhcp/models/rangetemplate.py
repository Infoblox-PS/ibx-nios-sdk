# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Rangetemplate - NIOS DHCP IPv4 range template.

All 65 properties from ``components.schemas.Rangetemplate`` in the v2.14 DHCP
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
        "uuid",
    }
)


class Rangetemplate(BaseModel):
    """NIOS DHCP IPv4 range template."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    bootfile: str | None = Field(
        default=None,
        description="The bootfile name for the range. You can configure the DHCP server to support clients that use the boot file name option in their DHCPREQUEST messages.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The bootserver address for the range. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
    )
    cloud_api_compatible: bool | None = Field(
        default=None,
        description="This flag controls whether this template can be used to create network objects in a cloud-computing deployment.",
    )
    comment: str | None = Field(
        default=None, description="A descriptive comment of a range template object."
    )
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this range.",
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    delegated_member: dict[str, Any] | None = Field(
        default=None,
        description="The Cloud Platform Appliance to which authority of the object is delegated.",
    )
    deny_all_clients: bool | None = Field(
        default=None, description="If True, send NAK forcing the client to take the new address."
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="Determines if BOOTP settings are disabled and BOOTP requests will be denied.",
    )
    email_list: list[str] | None = Field(
        default=None,
        description="The e-mail lists to which the appliance sends DHCP threshold alarm e-mail messages.",
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="Determines if the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_dhcp_thresholds: bool | None = Field(
        default=None, description="Determines if DHCP thresholds are enabled for the range."
    )
    enable_email_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are sent through email."
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    enable_snmp_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are sent through SNMP."
    )
    exclude: list[dict[str, Any]] | None = Field(
        default=None,
        description="These are ranges of IP addresses that the appliance does not use to assign to clients. You can use these exclusion addresses as static IP addresses. They contain the start and end addresses of the exclusion range, and optionally, information about this exclusion range.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    failover_association: str | None = Field(
        default=None,
        description="The name of the failover association: the server in this failover association will serve the IPv4 range in case the main server is out of service. {rangetemplate:rangetemplate} must be set to 'FAILOVER' or 'FAILOVER_MS' if you want the failover association specified here to serve the range.",
    )
    fingerprint_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the fingerprint filters for this DHCP range. The appliance uses matching rules in these filters to select the address range from which it assigns a lease.",
    )
    high_water_mark: int | None = Field(
        default=None,
        description="The percentage of DHCP range usage threshold above which range usage is not expected and may warrant your attention. When the high watermark is reached, the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    high_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage of DHCP range usage below which the corresponding SNMP trap is reset. A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The high watermark reset value must be lower than the high watermark value.",
    )
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="If this field is set to False, the appliance returns all DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )
    known_clients: Literal["Allow", "Deny"] | str | None = Field(
        default=None,
        description="Permission for known clients. If set to 'Deny' known clients will be denied IP addresses. Known clients include roaming hosts and clients with fixed addresses or DHCP host entries. Unknown clients include clients that are not roaming hosts and clients that do not have fixed addresses or DHCP host entries.",
    )
    lease_scavenge_time: int | None = Field(
        default=None,
        description="An integer that specifies the period of time (in seconds) that frees and backs up leases remained in the database before they are automatically deleted. To disable lease scavenging, set the parameter to -1. The minimum positive value must be greater than 86400 seconds (1 day).",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on this range. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )
    low_water_mark: int | None = Field(
        default=None,
        description="The percentage of DHCP range usage below which the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    low_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage of DHCP range usage threshold below which range usage is not expected and may warrant your attention. When the low watermark is crossed, the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The low watermark reset value must be higher than the low watermark value.",
    )
    mac_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the MAC filters to be applied to this range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    member: dict[str, Any] | None = Field(
        default=None, description="Reference to the Grid member that hosts this object."
    )
    ms_options: list[MsDhcpOption] | None = Field(
        default=None, description="The Microsoft DHCP options for this range."
    )
    ms_server: dict[str, Any] | None = Field(
        default=None, description="The primary Microsoft Server."
    )
    nac_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the NAC filters to be applied to this range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    name: str | None = Field(default=None, description="The name of a range template object.")
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address format of the next server that the host needs to boot.",
    )
    number_of_addresses: int | None = Field(
        default=None, description="The number of addresses for this range."
    )
    offset: int | None = Field(
        default=None, description="The start address offset for this range."
    )
    option_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the Option filters to be applied to this range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value for a range object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    recycle_leases: bool | None = Field(
        default=None,
        description="If the field is set to True, the leases are kept in the Recycle Bin until one week after expiration. Otherwise, the leases are permanently deleted.",
    )
    relay_agent_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the Relay Agent filters to be applied to this range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    server_association_type: (
        Literal["NONE", "MEMBER", "FAILOVER", "MS_SERVER", "MS_FAILOVER"] | str | None
    ) = Field(default=None, description="The type of server that is going to serve the range.")
    unknown_clients: Literal["Allow", "Deny"] | str | None = Field(
        default=None,
        description="Permission for unknown clients. If set to 'Deny' unknown clients will be denied IP addresses. Known clients include roaming hosts and clients with fixed addresses or DHCP host entries. Unknown clients include clients that are not roaming hosts and clients that do not have fixed addresses or DHCP host entries.",
    )
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_ddns_generate_hostname: bool | None = Field(
        default=None, description="Use flag for: ddns_generate_hostname"
    )
    use_deny_bootp: bool | None = Field(default=None, description="Use flag for: deny_bootp")
    use_email_list: bool | None = Field(default=None, description="Use flag for: email_list")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_enable_dhcp_thresholds: bool | None = Field(
        default=None, description="Use flag for: enable_dhcp_thresholds"
    )
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_known_clients: bool | None = Field(default=None, description="Use flag for: known_clients")
    use_lease_scavenge_time: bool | None = Field(
        default=None, description="Use flag for: lease_scavenge_time"
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
    use_recycle_leases: bool | None = Field(
        default=None, description="Use flag for: recycle_leases"
    )
    use_unknown_clients: bool | None = Field(
        default=None, description="Use flag for: unknown_clients"
    )
    use_update_dns_on_lease_renewal: bool | None = Field(
        default=None, description="Use flag for: update_dns_on_lease_renewal"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
