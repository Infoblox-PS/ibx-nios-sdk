# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Range - NIOS DHCP IPv4 range.

All 99 properties from ``components.schemas.Range`` in the v2.14 DHCP
swagger are represented here. Deeply nested types are inlined as dicts.

NOTE: The following complex nested schemas are inlined as dicts:
  - cloud_info
  - discovery_basic_poll_settings
  - discovery_blackout_setting
  - endpoint_sources (list)
  - exclude (list)
  - fingerprint_filter_rules (list)
  - logic_filter_rules (list)
  - mac_filter_rules (list)
  - member
  - ms_ad_user_data
  - ms_options (list)
  - nac_filter_rules (list)
  - next_available_ip (function schema)
  - option_filter_rules (list)
  - options (list)
  - port_control_blackout_setting
  - relay_agent_filter_rules (list)
  - split_member
  - subscribe_settings
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
        "dhcp_utilization",
        "dhcp_utilization_status",
        "discover_now_status",
        "dynamic_hosts",
        "endpoint_sources",
        "is_split_scope",
        "ms_ad_user_data",
        "static_hosts",
        "total_hosts",
        "uuid",
    }
)


class Range(BaseModel):
    """NIOS DHCP IPv4 range."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    always_update_dns: bool | None = Field(
        default=None,
        description="This field controls whether only the DHCP server is allowed to update DNS, regardless of the DHCP clients requests.",
    )
    bootfile: str | None = Field(
        default=None,
        description="The bootfile name for the range. You can configure the DHCP server to support clients that use the boot file name option in their DHCPREQUEST messages.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The bootserver address for the range. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
    )
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )
    comment: str | None = Field(
        default=None, description="Comment for the range; maximum 256 characters."
    )
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this range.",
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    deny_all_clients: bool | None = Field(
        default=None, description="If True, send NAK forcing the client to take the new address."
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="If set to true, BOOTP settings are disabled and BOOTP requests will be denied.",
    )  # read-only
    dhcp_utilization: int | None = Field(
        default=None,
        description="The percentage of the total DHCP utilization of the range multiplied by 1000. This is the percentage of the total number of available IP addresses belonging to the range versus the total number of all IP addresses in the range.",
    )
    dhcp_utilization_status: Literal["FULL", "HIGH", "LOW", "NORMAL"] | str | None = Field(
        default=None, description="A string describing the utilization level of the range."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a range is disabled or not. When this is set to False, the range is enabled.",
    )  # read-only
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(default=None, description="Discover now status for this range.")
    discovery_basic_poll_settings: dict[str, Any] | None = Field(
        default=None, description="Basic discovery polling settings."
    )
    discovery_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Discovery blackout schedule for this object."
    )
    discovery_member: str | None = Field(
        default=None, description="The member that will run discovery for this range."
    )  # read-only
    dynamic_hosts: int | None = Field(
        default=None, description="The total number of DHCP leases issued for the range."
    )
    email_list: list[str] | None = Field(
        default=None,
        description="The e-mail lists to which the appliance sends DHCP threshold alarm e-mail messages.",
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP range object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_dhcp_thresholds: bool | None = Field(
        default=None, description="Determines if DHCP thresholds are enabled for the range."
    )
    enable_discovery: bool | None = Field(
        default=None,
        description="Determines whether a discovery is enabled or not for this range. When this is set to False, the discovery for this range is disabled.",
    )
    enable_email_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are sent through email."
    )
    enable_ifmap_publishing: bool | None = Field(
        default=None, description="Determines if IFMAP publishing is enabled for the range."
    )
    enable_immediate_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the range should be immediately enabled.",
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    enable_snmp_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are send through SNMP."
    )
    end_addr: str | None = Field(
        default=None, description="The IPv4 Address end address of the range."
    )  # read-only
    endpoint_sources: list[dict[str, Any] | str] | None = Field(
        default=None, description="The endpoints that provides data for the DHCP Range object."
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
        description="The name of the failover association: the server in this failover association will serve the IPv4 range in case the main server is out of service. {range:range} must be set to 'FAILOVER' or 'FAILOVER_MS' if you want the failover association specified here to serve the range.",
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
    ignore_id: Literal["NONE", "CLIENT", "MACADDR"] | str | None = Field(
        default=None,
        description='Indicates whether the appliance will ignore DHCP client IDs or MAC addresses. Valid values are "NONE", "CLIENT", or "MACADDR". The default is "NONE".',
    )
    ignore_mac_addresses: list[str] | None = Field(
        default=None, description="A list of MAC addresses the appliance will ignore."
    )  # read-only
    is_split_scope: bool | None = Field(
        default=None,
        description="This field will be 'true' if this particular range is part of a split scope.",
    )
    known_clients: str | None = Field(
        default=None,
        description="Permission for known clients. This can be 'Allow' or 'Deny'. If set to 'Deny' known clients will be denied IP addresses. Known clients include roaming hosts and clients with fixed addresses or DHCP host entries. Unknown clients include clients that are not roaming hosts and clients that do not have fixed addresses or DHCP host entries.",
    )
    lease_scavenge_time: int | None = Field(
        default=None,
        description="An integer that specifies the period of time (in seconds) that frees and backs up leases remained in the database before they are automatically deleted. To disable lease scavenging, set the parameter to -1. The minimum positive value must be greater than 86400 seconds (1 day).",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied to this range. This list corresponds to the match rules that are written to the dhcpd configuration file.",
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
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )
    ms_options: list[MsDhcpOption] | None = Field(
        default=None, description="This field contains the Microsoft DHCP options for this range."
    )
    ms_server: dict[str, Any] | None = Field(
        default=None, description="The primary Microsoft Server."
    )
    nac_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the NAC filters to be applied to this range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    name: str | None = Field(
        default=None, description="This field contains the name of the Microsoft scope."
    )
    network: str | None = Field(
        default=None,
        description="The network to which this range belongs, in IPv4 Address/CIDR format.",
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this range resides."
    )
    next_available_ip: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the next-available-IP operation."
    )
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address of the next server that the host needs to boot.",
    )
    option_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the Option filters to be applied to this range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    port_control_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Port-control blackout schedule for this object."
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value of a DHCP Range object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    recycle_leases: bool | None = Field(
        default=None,
        description="If the field is set to True, the leases are kept in the Recycle Bin until one week after expiration. Otherwise, the leases are permanently deleted.",
    )
    relay_agent_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the Relay Agent filters to be applied to this range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    restart_if_needed: bool | None = Field(
        default=None, description="Restarts the member service."
    )
    same_port_control_discovery_blackout: bool | None = Field(
        default=None,
        description="If the field is set to True, the discovery blackout setting will be used for port control blackout setting.",
    )
    server_association_type: (
        Literal["NONE", "MEMBER", "FAILOVER", "MS_SERVER", "MS_FAILOVER"] | str | None
    ) = Field(default=None, description="The type of server that is going to serve the range.")
    split_member: dict[str, Any] | None = Field(default=None)
    split_scope_exclusion_percent: int | None = Field(
        default=None,
        description="This field controls the percentage used when creating a split scope. Valid values are numbers between 1 and 99. If the value is 40, it means that the top 40% of the exclusion will be created on the DHCP range assigned to {next_available_ip:next_available_ip} and the lower 60% of the range will be assigned to DHCP range assigned to {next_available_ip:next_available_ip}",
    )
    start_addr: str | None = Field(
        default=None, description="The IPv4 Address starting address of the range."
    )  # read-only
    static_hosts: int | None = Field(
        default=None, description="The number of static DHCP addresses configured in the range."
    )
    subscribe_settings: dict[str, Any] | None = Field(
        default=None,
        description="Subscription settings for receiving updates from upstream sources.",
    )
    template: str | None = Field(
        default=None,
        description="If set on creation, the range will be created according to the values specified in the named template.",
    )  # read-only
    total_hosts: int | None = Field(
        default=None, description="The total number of DHCP addresses configured in the range."
    )
    unknown_clients: str | None = Field(
        default=None,
        description="Permission for unknown clients. This can be 'Allow' or 'Deny'. If set to 'Deny', unknown clients will be denied IP addresses. Known clients include roaming hosts and clients with fixed addresses or DHCP host entries. Unknown clients include clients that are not roaming hosts and clients that do not have fixed addresses or DHCP host entries.",
    )
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )
    use_blackout_setting: bool | None = Field(
        default=None,
        description="Use flag for: discovery_blackout_setting , port_control_blackout_setting, same_port_control_discovery_blackout",
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
    use_discovery_basic_polling_settings: bool | None = Field(
        default=None, description="Use flag for: discovery_basic_poll_settings"
    )
    use_email_list: bool | None = Field(default=None, description="Use flag for: email_list")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_enable_dhcp_thresholds: bool | None = Field(
        default=None, description="Use flag for: enable_dhcp_thresholds"
    )
    use_enable_discovery: bool | None = Field(
        default=None, description="Use flag for: discovery_member , enable_discovery"
    )
    use_enable_ifmap_publishing: bool | None = Field(
        default=None, description="Use flag for: enable_ifmap_publishing"
    )
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_ignore_id: bool | None = Field(default=None, description="Use flag for: ignore_id")
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
    use_subscribe_settings: bool | None = Field(
        default=None, description="Use flag for: subscribe_settings"
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
