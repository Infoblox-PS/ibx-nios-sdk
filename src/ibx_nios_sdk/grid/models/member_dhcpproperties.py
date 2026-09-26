# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberDhcpproperties - NIOS member DHCP properties (subset of key fields).

Many fields in this object. We include those from the swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, LogicFilterRule

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "dhcp_utilization",
        "dhcp_utilization_status",
        "dynamic_hosts",
        "failover_association_ip_count",
        "failover_association_utilization",
        "host_name",
        "ipv4addr",
        "ipv6addr",
        "static_hosts",
        "total_hosts",
        "uuid",
    }
)


class MemberDhcpproperties(BaseModel):
    """NIOS member DHCP properties."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    auth_server_group: str | None = Field(
        default=None,
        description="The Authentication Server Group object associated with this member.",
    )
    authn_captive_portal: str | None = Field(
        default=None,
        description="The captive portal responsible for authenticating this DHCP member.",
    )
    authn_captive_portal_authenticated_filter: str | None = Field(
        default=None, description="The MAC filter representing the authenticated range."
    )
    authn_captive_portal_enabled: bool | None = Field(
        default=None,
        description="The flag that controls if this DHCP member is enabled for captive portal authentication.",
    )
    authn_captive_portal_guest_filter: str | None = Field(
        default=None, description="The MAC filter representing the guest range."
    )
    authn_server_group_enabled: bool | None = Field(
        default=None,
        description="The flag that controls if this DHCP member can send authentication requests to an authentication server group.",
    )
    authority: bool | None = Field(
        default=None,
        description="The authority flag of a Grid member. This flag specifies if a DHCP server is authoritative for a domain.",
    )
    bootfile: str | None = Field(
        default=None,
        description="The name of a file that DHCP clients need to boot. This setting overrides the Grid level setting.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The name of the server on which a boot file is stored. This setting overrides the Grid level setting.",
    )
    ddns_domainname: str | None = Field(
        default=None, description="The member DDNS domain name value."
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="Determines the ability of a member DHCP server to generate a host name and update DNS with this host name when it receives a DHCP REQUEST message that does not include a host name.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="Determines that only the DHCP server is allowed to update DNS, regardless of the requests from the DHCP clients. This setting overrides the Grid level setting.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DDNS TTL (Dynamic DNS Time To Live) value specifies the number of seconds an IP address for the name is cached.",
    )
    ddns_update_fixed_addresses: bool | None = Field(
        default=None,
        description="Determines if the member DHCP server's ability to update the A and PTR records with a fixed address is enabled or not.",
    )
    ddns_use_option81: bool | None = Field(
        default=None, description="Determines if support for option 81 is enabled or not."
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="Determines if a BOOTP server denies BOOTP request or not. This setting overrides the Grid level setting.",
    )
    dhcp_utilization: int | None = Field(
        default=None,
        description="The percentage of the total DHCP utilization of DHCP objects belonging to the Grid Member multiplied by 1000. This is the percentage of the total number of available IP addresses from all the DHCP objects belonging to the Grid Member versus the total number of all IP addresses in all of the DHCP objects on the Grid Member.",
    )
    dhcp_utilization_status: Literal["FULL", "HIGH", "LOW", "NORMAL"] | str | None = Field(
        default=None,
        description="A string describing the utilization level of DHCP objects that belong to the Grid Member.",
    )
    dynamic_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP leases issued for the DHCP objects on the Grid Member.",
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="Determines if the member DHCP server's ability to send DDNS updates is enabled or not.",
    )
    enable_dhcp_thresholds: bool | None = Field(
        default=None,
        description="Represents the watermarks above or below which address usage in a network is unexpected and might warrant your attention. This setting overrides the Grid level setting.",
    )
    enable_email_warnings: bool | None = Field(
        default=None,
        description="Determines if e-mail warnings are enabled or disabled. When DHCP threshold is enabled and DHCP address usage crosses a watermark threshold, the appliance sends an e-mail notification to an administrator.",
    )
    enable_fingerprint: bool | None = Field(
        default=None,
        description="Determines if fingerprint feature is enabled on this member. If you enable this feature, the server will match a fingerprint for incoming lease requests.",
    )
    enable_gss_tsig: bool | None = Field(
        default=None,
        description="Determines whether the appliance is enabled to receive GSS-TSIG authenticated updates from DHCP clients.",
    )
    enable_hostname_rewrite: bool | None = Field(
        default=None,
        description="Determines if the Grid member's host name rewrite feature is enabled or not.",
    )
    enable_leasequery: bool | None = Field(
        default=None,
        description="Determines if lease query is allowed or not. This setting overrides the Grid-level setting.",
    )
    enable_snmp_warnings: bool | None = Field(
        default=None,
        description="Determines if SNMP warnings are enabled or disabled on this DHCP member. When DHCP threshold is enabled and DHCP address usage crosses a watermark threshold, the appliance sends an SNMP trap to the trap receiver that was defined for the Grid member level.",
    )
    failover_association_ip_count: int | None = Field(
        default=None,
        description="Total number of IPs associated with IPv4 DHCP failover associations for the member.",
    )
    failover_association_utilization: float | None = Field(
        default=None, description="Failover association utilization percentage."
    )
    gss_tsig_keys: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of GSS-TSIG keys for a member DHCP object."
    )
    high_water_mark: int | None = Field(
        default=None,
        description="Determines the high watermark value of a member DHCP server. If the percentage of allocated addresses exceeds this watermark, the appliance makes a syslog entry and sends an e-mail notification (if enabled). Specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    high_water_mark_reset: int | None = Field(
        default=None,
        description="Determines the high watermark reset value of a member DHCP server. If the percentage of allocated addresses drops below this value, a corresponding SNMP trap is reset. Specifies the percentage of allocated addresses. The range is from 1 to 100. The high watermark reset value must be lower than the high watermark value.",
    )
    host_name: str | None = Field(default=None, description="Host name of the Grid member.")
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="Determines if the ignore DHCP option list request flag of a Grid member DHCP is enabled or not. If this flag is set to true all available DHCP options will be returned to the client.",
    )
    ignore_id: Literal["NONE", "CLIENT", "MACADDR"] | str | None = Field(
        default=None,
        description='Indicates whether the appliance will ignore DHCP client IDs or MAC addresses. Valid values are "NONE", "CLIENT", or "MACADDR". The default is "NONE".',
    )
    ipv4addr: str | None = Field(default=None, description="The IPv4 Address of the Grid member.")
    ipv6addr: str | None = Field(default=None, description="The IPv6 Address of the Grid member.")
    ipv6_ddns_domainname: str | None = Field(
        default=None, description="The member DDNS IPv6 domain name value."
    )
    ipv6_ddns_enable_option_fqdn: bool | None = Field(
        default=None,
        description="Controls whether the FQDN option sent by the DHCPv6 client is to be used, or if the server can automatically generate the FQDN.",
    )
    ipv6_ddns_server_always_updates: bool | None = Field(
        default=None,
        description="Determines if the server always updates DNS or updates only if requested by the client.",
    )
    ipv6_ddns_ttl: int | None = Field(default=None, description="The member IPv6 DDNS TTL value.")
    ipv6_domain_name: str | None = Field(default=None, description="The IPv6 domain name.")
    ipv6_domain_name_servers: list[str] | None = Field(
        default=None,
        description="The comma separated list of domain name server addresses in IPv6 address format.",
    )
    ipv6_enable_ddns: bool | None = Field(
        default=None,
        description="Determines if sending DDNS updates by the member DHCPv6 server is enabled or not.",
    )
    ipv6_enable_gss_tsig: bool | None = Field(
        default=None,
        description="Determines whether the appliance is enabled to receive GSS-TSIG authenticated updates from DHCPv6 clients.",
    )
    ipv6_generate_hostname: bool | None = Field(
        default=None,
        description="Determines if the server generates the hostname if it is not sent by the client.",
    )
    ipv6_gss_tsig_keys: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of GSS-TSIG keys for a member DHCPv6 object."
    )
    ipv6_kdc_server: str | None = Field(
        default=None,
        description="Determines the IPv6 address or FQDN of the Kerberos server for DHCPv6 GSS-TSIG authentication. This setting overrides the Grid level setting.",
    )
    ipv6_options: list[dict[str, Any]] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCPv6 options associated with the object.",
    )
    ipv6_recycle_leases: bool | None = Field(
        default=None,
        description="Determines if the IPv6 recycle leases feature is enabled or not. If the feature is enabled, leases are kept in the Recycle Bin until one week after lease expiration. When the feature is disabled, the leases are irrecoverably deleted.",
    )
    kdc_server: str | None = Field(
        default=None,
        description="The IPv4 address or FQDN of the Kerberos server for DHCPv4 GSS-TSIG authentication. This setting overrides the Grid level setting.",
    )
    lease_scavenge_time: int | None = Field(
        default=None,
        description="Determines the lease scavenging time value. When this field is set, the appliance permanently deletes the free and backup leases that remain in the database beyond a specified period of time. To disable lease scavenging, set the parameter to -1. The minimum positive value must be greater than 86400 seconds (1 day).",
    )
    log_lease_events: bool | None = Field(
        default=None,
        description="This value specifies whether the grid member logs lease events. This setting overrides the Grid level setting.",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the Grid member. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )
    low_water_mark: int | None = Field(
        default=None,
        description="Determines the low watermark value. If the percent of allocated addresses drops below this watermark, the appliance makes a syslog entry and sends an e-mail notification (if enabled).",
    )
    low_water_mark_reset: int | None = Field(
        default=None,
        description="Determines the low watermark reset value. If the percentage of allocated addresses exceeds this value, a corresponding SNMP trap is reset. A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The low watermark reset value must be higher than the low watermark value.",
    )
    nextserver: str | None = Field(
        default=None,
        description="The next server value of a member DHCP server. This value is the IP address or name of the boot file server on which the boot file is stored.",
    )
    option60_match_rules: list[dict[str, Any]] | None = Field(
        default=None, description="The list of option 60 match rules."
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    ping_count: int | None = Field(
        default=None,
        description="Specifies the number of pings that the Infoblox appliance sends to an IP address to verify that it is not in use. Values are from 0 to 10, where 0 disables pings.",
    )
    ping_timeout: int | None = Field(
        default=None,
        description="Indicates the number of milliseconds the appliance waits for a response to its ping. Valid values are 100, 500, 1000, 2000, 3000, 4000 and 5000 milliseconds.",
    )
    preferred_lifetime: int | None = Field(
        default=None, description="The preferred lifetime value."
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="Specifies the duration of time it takes a host to connect to a boot server, such as a TFTP server, and download the file it needs to boot. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    recycle_leases: bool | None = Field(
        default=None,
        description="Determines if the recycle leases feature is enabled or not. If you enabled this feature and then delete a DHCP range, the appliance stores active leases from this range up to one week after the leases expires.",
    )
    retry_ddns_updates: bool | None = Field(
        default=None,
        description="Indicates whether the DHCP server makes repeated attempts to send DDNS updates to a DNS server.",
    )
    static_hosts: int | None = Field(
        default=None,
        description="The number of static DHCP addresses configured in DHCP objects that belong to the Grid Member.",
    )
    syslog_facility: (
        Literal[
            "DAEMON",
            "LOCAL0",
            "LOCAL1",
            "LOCAL2",
            "LOCAL3",
            "LOCAL4",
            "LOCAL5",
            "LOCAL6",
            "LOCAL7",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The syslog facility is the location on the syslog server to which you want to sort the syslog messages.",
    )
    total_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP addresses configured in DHCP objects that belong to the Grid Member.",
    )
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="Controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_lifetime: int | None = Field(
        default=None,
        description="The valid lifetime for Grid Member DHCP. Specifies the length of time addresses that are assigned to DHCPv6 clients remain in the valid state.",
    )
    clear_nac_auth_cache: object | None = Field(default=None)
    ddns_retry_interval: int | None = Field(default=None)
    ddns_zone_primaries: object | None = Field(default=None)
    dns_update_style: Literal["INTERIM", "STANDARD"] | str | None = Field(default=None)
    email_list: list[str] | None = Field(default=None)
    enable_dhcp: bool | None = Field(default=None)
    enable_dhcp_on_ipv6_lan2: bool | None = Field(default=None)
    enable_dhcp_on_lan2: bool | None = Field(default=None)
    enable_dhcpv6_service: bool | None = Field(default=None)
    extattrs: object | None = Field(
        default=None, description="Extensible attributes (key/value tags) attached to the object."
    )
    hostname_rewrite_policy: str | None = Field(default=None)
    ignore_mac_addresses: list[str] | None = Field(default=None)
    immediate_fa_configuration: bool | None = Field(default=None)
    ipv6_ddns_hostname: str | None = Field(default=None)
    ipv6_dns_update_style: Literal["INTERIM", "STANDARD"] | str | None = Field(default=None)
    ipv6_enable_lease_scavenging: bool | None = Field(default=None)
    ipv6_enable_retry_updates: bool | None = Field(default=None)
    ipv6_lease_scavenging_time: int | None = Field(default=None)
    ipv6_microsoft_code_page: (
        Literal[
            "None",
            "US (437)",
            "Greek (737)",
            "Baltic (775)",
            "Multilingual Latin I (850)",
            "Latin II (852)",
            "Cyrillic (855)",
            "Turkish (857)",
            "Hebrew (862)",
            "Russian (866)",
            "Thai (874)",
            "Japanese Shift-JIS (932)",
            "Simplified Chinese GBK (936)",
            "Korean (949)",
            "Traditional Chinese Big5 (950)",
            "Central Europe (1250)",
            "Cyrillic (1251)",
            "Latin I (1252)",
            "Greek (1253)",
            "Turkish (1254)",
            "Hebrew (1255)",
            "Arabic (1256)",
            "Baltic (1257)",
            "Vietnam (1258)",
            "Latin 1 (ISO-8859-1)",
            "Latin 2 (ISO-8859-2)",
            "Latin 3 (ISO-8859-3)",
            "Baltic (ISO-8859-4)",
            "Cyrillic (ISO-8859-5)",
            "Arabic (ISO-8859-6)",
            "Greek (ISO-8859-7)",
            "Hebrew (ISO-8859-8)",
            "Turkish (ISO-8859-9)",
            "Latin 9 (ISO-8859-15)",
        ]
        | str
        | None
    ) = Field(default=None)
    ipv6_remember_expired_client_association: bool | None = Field(default=None)
    ipv6_retry_updates_interval: int | None = Field(default=None)
    ipv6_server_duid: str | None = Field(default=None)
    ipv6_update_dns_on_lease_renewal: bool | None = Field(default=None)
    lease_per_client_settings: (
        Literal["RELEASE_MATCHING_ID", "NEVER_RELEASE", "ONE_LEASE_PER_CLIENT"] | str | None
    ) = Field(default=None)
    max_failover_association_ip_count: int | None = Field(default=None)
    microsoft_code_page: (
        Literal[
            "None",
            "US (437)",
            "Greek (737)",
            "Baltic (775)",
            "Multilingual Latin I (850)",
            "Latin II (852)",
            "Cyrillic (855)",
            "Turkish (857)",
            "Hebrew (862)",
            "Russian (866)",
            "Thai (874)",
            "Japanese Shift-JIS (932)",
            "Simplified Chinese GBK (936)",
            "Korean (949)",
            "Traditional Chinese Big5 (950)",
            "Central Europe (1250)",
            "Cyrillic (1251)",
            "Latin I (1252)",
            "Greek (1253)",
            "Turkish (1254)",
            "Hebrew (1255)",
            "Arabic (1256)",
            "Baltic (1257)",
            "Vietnam (1258)",
            "Latin 1 (ISO-8859-1)",
            "Latin 2 (ISO-8859-2)",
            "Latin 3 (ISO-8859-3)",
            "Baltic (ISO-8859-4)",
            "Cyrillic (ISO-8859-5)",
            "Arabic (ISO-8859-6)",
            "Greek (ISO-8859-7)",
            "Hebrew (ISO-8859-8)",
            "Turkish (ISO-8859-9)",
            "Latin 9 (ISO-8859-15)",
        ]
        | str
        | None
    ) = Field(default=None)
    prefix_length_mode: Literal["EXACT", "IGNORE", "MINIMUM", "MAXIMUM", "PREFER"] | str | None = (
        Field(default=None)
    )
    purge_ifmap_data: object | None = Field(default=None)
    use_authority: bool | None = Field(default=None)
    use_bootfile: bool | None = Field(default=None)
    use_bootserver: bool | None = Field(default=None)
    use_ddns_domainname: bool | None = Field(default=None)
    use_ddns_generate_hostname: bool | None = Field(default=None)
    use_ddns_ttl: bool | None = Field(default=None)
    use_ddns_update_fixed_addresses: bool | None = Field(default=None)
    use_ddns_use_option81: bool | None = Field(default=None)
    use_deny_bootp: bool | None = Field(default=None)
    use_dns_update_style: bool | None = Field(default=None)
    use_email_list: bool | None = Field(default=None)
    use_enable_ddns: bool | None = Field(default=None)
    use_enable_dhcp_thresholds: bool | None = Field(default=None)
    use_enable_fingerprint: bool | None = Field(default=None)
    use_enable_gss_tsig: bool | None = Field(
        default=None, description="Override flag controlling whether GSS-TSIG is enabled."
    )
    use_enable_hostname_rewrite: bool | None = Field(default=None)
    use_enable_leasequery: bool | None = Field(default=None)
    use_enable_one_lease_per_client: bool | None = Field(default=None)
    use_gss_tsig_keys: bool | None = Field(
        default=None, description="Override flag controlling whether GSS-TSIG keys are honored."
    )
    use_ignore_dhcp_option_list_request: bool | None = Field(default=None)
    use_ignore_id: bool | None = Field(default=None)
    use_immediate_fa_configuration: bool | None = Field(default=None)
    use_ipv6_ddns_domainname: bool | None = Field(default=None)
    use_ipv6_ddns_enable_option_fqdn: bool | None = Field(default=None)
    use_ipv6_ddns_hostname: bool | None = Field(default=None)
    use_ipv6_ddns_ttl: bool | None = Field(default=None)
    use_ipv6_dns_update_style: bool | None = Field(default=None)
    use_ipv6_domain_name: bool | None = Field(default=None)
    use_ipv6_domain_name_servers: bool | None = Field(default=None)
    use_ipv6_enable_ddns: bool | None = Field(default=None)
    use_ipv6_enable_gss_tsig: bool | None = Field(default=None)
    use_ipv6_enable_retry_updates: bool | None = Field(default=None)
    use_ipv6_generate_hostname: bool | None = Field(default=None)
    use_ipv6_gss_tsig_keys: bool | None = Field(default=None)
    use_ipv6_lease_scavenging: bool | None = Field(default=None)
    use_ipv6_microsoft_code_page: bool | None = Field(default=None)
    use_ipv6_options: bool | None = Field(default=None)
    use_ipv6_recycle_leases: bool | None = Field(default=None)
    use_ipv6_update_dns_on_lease_renewal: bool | None = Field(default=None)
    use_lease_per_client_settings: bool | None = Field(default=None)
    use_lease_scavenge_time: bool | None = Field(default=None)
    use_log_lease_events: bool | None = Field(default=None)
    use_logic_filter_rules: bool | None = Field(default=None)
    use_microsoft_code_page: bool | None = Field(default=None)
    use_nextserver: bool | None = Field(default=None)
    use_options: bool | None = Field(default=None)
    use_ping_count: bool | None = Field(default=None)
    use_ping_timeout: bool | None = Field(default=None)
    use_preferred_lifetime: bool | None = Field(default=None)
    use_prefix_length_mode: bool | None = Field(default=None)
    use_pxe_lease_time: bool | None = Field(default=None)
    use_recycle_leases: bool | None = Field(default=None)
    use_retry_ddns_updates: bool | None = Field(default=None)
    use_syslog_facility: bool | None = Field(
        default=None,
        description="Override flag controlling whether the configured syslog facility is used.",
    )
    use_update_dns_on_lease_renewal: bool | None = Field(default=None)
    use_valid_lifetime: bool | None = Field(default=None)
