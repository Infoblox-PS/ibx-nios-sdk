# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridDhcpproperties - NIOS Grid DHCP properties.

All properties from ``components.schemas.GridDhcpproperties`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, LogicFilterRule

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "grid",
        "uuid",
    }
)


class GridDhcpproperties(BaseModel):
    """NIOS Grid DHCP properties."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    authority: bool | None = Field(
        default=None,
        description="The Grid-level authority flag. This flag specifies whether a DHCP server is authoritative for a domain.",
    )
    bootfile: str | None = Field(
        default=None,
        description="The name of a file that DHCP clients need to boot. Some DHCP clients use BOOTP (bootstrap protocol) or include the boot file name option in their DHCPREQUEST messages.",
    )
    bootserver: str | None = Field(
        default=None, description="The name of the server on which a boot file is stored."
    )
    capture_hostname: bool | None = Field(
        default=None,
        description="The Grid-level capture hostname flag. Set this flag to capture the hostname and lease time when assigning a fixed address.",
    )
    ddns_domainname: str | None = Field(
        default=None, description="The member DDNS domain name value."
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="Determines if the ability of a DHCP server to generate a host name and update DNS with this host name when it receives a DHCP REQUEST message that does not include a host name is enabled or not.",
    )
    ddns_retry_interval: int | None = Field(
        default=None,
        description="Determines the retry interval when the DHCP server makes repeated attempts to send DDNS updates to a DNS server.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="Determines that only the DHCP server is allowed to update DNS, regardless of the requests from the DHCP clients.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DDNS TTL (Dynamic DNS Time To Live) value specifies the number of seconds an IP address for the name is cached.",
    )
    ddns_update_fixed_addresses: bool | None = Field(
        default=None,
        description="Determines if the Grid DHCP server's ability to update the A and PTR records with a fixed address is enabled or not.",
    )
    ddns_use_option81: bool | None = Field(
        default=None, description="Determines if support for option 81 is enabled or not."
    )
    deny_bootp: bool | None = Field(
        default=None, description="Determines if deny BOOTP is enabled or not."
    )
    disable_all_nac_filters: bool | None = Field(
        default=None,
        description="If set to True, NAC filters will be disabled on the Infoblox Grid.",
    )
    dns_update_style: Literal["INTERIM", "STANDARD"] | str | None = Field(
        default=None, description="The update style for dynamic DNS updates."
    )
    email_list: list[str] | None = Field(
        default=None,
        description="The Grid-level email_list value. Specify an e-mail address to which you want the Infoblox appliance to send e-mail notifications when the DHCP address usage for the grid crosses a threshold. You can create a list of several e-mail addresses.",
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="Determines if the member DHCP server's ability to send DDNS updates is enabled or not.",
    )
    enable_dhcp_thresholds: bool | None = Field(
        default=None,
        description="Represents the watermarks above or below which address usage in a network is unexpected and might warrant your attention.",
    )
    enable_email_warnings: bool | None = Field(
        default=None,
        description="Determines if e-mail warnings are enabled or disabled. When DHCP threshold is enabled and DHCP address usage crosses a watermark threshold, the appliance sends an e-mail notification to an administrator.",
    )
    enable_fingerprint: bool | None = Field(
        default=None,
        description="Determines if the fingerprint feature is enabled or not. If you enable this feature, the server will match a fingerprint for incoming lease requests.",
    )
    enable_gss_tsig: bool | None = Field(
        default=None,
        description="Determines whether all appliances are enabled to receive GSS-TSIG authenticated updates from DHCP clients.",
    )
    enable_hostname_rewrite: bool | None = Field(
        default=None,
        description="Determines if the Grid-level host name rewrite feature is enabled or not.",
    )
    enable_leasequery: bool | None = Field(
        default=None, description="Determines if lease query is allowed or not."
    )
    enable_roaming_hosts: bool | None = Field(
        default=None,
        description="Determines if DHCP servers in a Grid support roaming hosts or not.",
    )
    enable_snmp_warnings: bool | None = Field(
        default=None,
        description="Determined if the SNMP warnings on Grid-level are enabled or not. When DHCP threshold is enabled and DHCP address usage crosses a watermark threshold, the appliance sends an SNMP trap to the trap receiver that you defined you defined at the Grid member level.",
    )
    format_log_option_82: Literal["HEX", "TEXT"] | str | None = Field(
        default=None, description="The format option for Option 82 logging."
    )  # read-only
    grid: str | None = Field(
        default=None,
        description="Determines the Grid that serves DHCP. This specifies a group of Infoblox appliances that are connected together to provide a single point of device administration and service configuration in a secure, highly available environment.",
    )
    gss_tsig_keys: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of GSS-TSIG keys for a Grid DHCP object."
    )
    high_water_mark: int | None = Field(
        default=None,
        description="Determines the high watermark value of a Grid DHCP server. If the percentage of allocated addresses exceeds this watermark, the appliance makes a syslog entry and sends an e-mail notification (if enabled). Specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    high_water_mark_reset: int | None = Field(
        default=None,
        description="Determines the high watermark reset value of a member DHCP server. If the percentage of allocated addresses drops below this value, a corresponding SNMP trap is reset. Specifies the percentage of allocated addresses. The range is from 1 to 100. The high watermark reset value must be lower than the high watermark value.",
    )
    hostname_rewrite_policy: str | None = Field(
        default=None,
        description="The name of the default hostname rewrite policy, which is also in the protocol_hostname_rewrite_policies array.",
    )
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="Determines if the ignore DHCP option list request flag of a Grid DHCP is enabled or not. If this flag is set to true all available DHCP options will be returned to the client.",
    )
    ignore_id: Literal["NONE", "CLIENT", "MACADDR"] | str | None = Field(
        default=None,
        description='Indicates whether the appliance will ignore DHCP client IDs or MAC addresses. Valid values are "NONE", "CLIENT", or "MACADDR". The default is "NONE".',
    )
    ignore_mac_addresses: list[str] | None = Field(
        default=None, description="A list of MAC addresses the appliance will ignore."
    )
    immediate_fa_configuration: bool | None = Field(
        default=None,
        description="Determines if the fixed address configuration takes effect immediately without DHCP service restart or not.",
    )
    ipv6_capture_hostname: bool | None = Field(
        default=None,
        description="Determines if the IPv6 host name and lease time is captured or not while assigning a fixed address.",
    )
    ipv6_ddns_domainname: str | None = Field(
        default=None, description="The Grid-level DDNS domain name value."
    )
    ipv6_ddns_enable_option_fqdn: bool | None = Field(
        default=None,
        description="Controls whether the FQDN option sent by the client is to be used, or if the server can automatically generate the FQDN.",
    )
    ipv6_ddns_server_always_updates: bool | None = Field(
        default=None,
        description="Determines if the server always updates DNS or updates only if requested by the client.",
    )
    ipv6_ddns_ttl: int | None = Field(
        default=None, description="The Grid-level IPv6 DDNS TTL value."
    )
    ipv6_default_prefix: str | None = Field(
        default=None, description="The Grid-level IPv6 default prefix."
    )
    ipv6_dns_update_style: Literal["INTERIM", "STANDARD"] | str | None = Field(
        default=None, description="The update style for dynamic DHCPv6 DNS updates."
    )
    ipv6_domain_name: str | None = Field(default=None, description="The IPv6 domain name.")
    ipv6_domain_name_servers: list[str] | None = Field(
        default=None,
        description="The comma separated list of domain name server addresses in IPv6 address format.",
    )
    ipv6_enable_ddns: bool | None = Field(
        default=None,
        description="Determines if sending DDNS updates by the DHCPv6 server is enabled or not.",
    )
    ipv6_enable_gss_tsig: bool | None = Field(
        default=None,
        description="Determines whether the all appliances are enabled to receive GSS-TSIG authenticated updates from DHCPv6 clients.",
    )
    ipv6_enable_lease_scavenging: bool | None = Field(
        default=None,
        description="Indicates whether DHCPv6 lease scavenging is enabled or disabled.",
    )
    ipv6_enable_retry_updates: bool | None = Field(
        default=None,
        description="Determines if the DHCPv6 server retries failed dynamic DNS updates or not.",
    )
    ipv6_generate_hostname: bool | None = Field(
        default=None,
        description="Determines if the server generates the hostname if it is not sent by the client.",
    )
    ipv6_gss_tsig_keys: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of GSS-TSIG keys for a Grid DHCPv6 object."
    )
    ipv6_kdc_server: str | None = Field(
        default=None,
        description="The IPv6 address or FQDN of the Kerberos server for DHCPv6 GSS-TSIG authentication.",
    )
    ipv6_lease_scavenging_time: int | None = Field(
        default=None,
        description="The Grid-level grace period (in seconds) to keep an expired lease before it is deleted by the scavenging process.",
    )
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
    ) = Field(
        default=None,
        description="The Grid-level Microsoft client DHCP IPv6 code page value. This value is the hostname translation code page for Microsoft DHCP IPv6 clients.",
    )
    ipv6_options: list[dict[str, Any]] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCPv6 options associated with the object.",
    )
    ipv6_prefixes: list[str] | None = Field(
        default=None, description="The Grid-level list of IPv6 prefixes."
    )
    ipv6_recycle_leases: bool | None = Field(
        default=None,
        description="Determines if the IPv6 recycle leases feature is enabled or not. If the feature is enabled, leases are kept in the Recycle Bin until one week after expiration. When the feature is disabled, the leases are irrecoverably deleted.",
    )
    ipv6_remember_expired_client_association: bool | None = Field(
        default=None, description="Enable binding for expired DHCPv6 leases."
    )
    ipv6_retry_updates_interval: int | None = Field(
        default=None,
        description="Determines the retry interval when the member DHCPv6 server makes repeated attempts to send DDNS updates to a DNS server.",
    )
    ipv6_txt_record_handling: (
        Literal["ISC", "ISC_TRANSITIONAL", "IGNORE_CONTENTS", "MS"] | str | None
    ) = Field(
        default=None,
        description="The Grid-level TXT record handling value. This value specifies how DHCPv6 should treat the TXT records when performing DNS updates.",
    )
    ipv6_update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="Controls whether the DHCPv6 server updates DNS when an IPv6 DHCP lease is renewed.",
    )
    kdc_server: str | None = Field(
        default=None,
        description="The IPv4 address or FQDN of the Kerberos server for DHCPv4 GSS-TSIG authentication.",
    )
    lease_logging_member: str | None = Field(
        default=None,
        description="The Grid member on which you want to store the DHCP lease history log. Infoblox recommends that you dedicate a member other than the master as a logging member. If possible, use this member solely for storing the DHCP lease history log. If you do not select a member, no logging can occur.",
    )
    lease_per_client_settings: (
        Literal["RELEASE_MATCHING_ID", "NEVER_RELEASE", "ONE_LEASE_PER_CLIENT"] | str | None
    ) = Field(
        default=None,
        description='Defines how the appliance releases DHCP leases. Valid values are "RELEASE_MACHING_ID", "NEVER_RELEASE", or "ONE_LEASE_PER_CLIENT". The default is "RELEASE_MATCHING_ID".',
    )
    lease_scavenge_time: int | None = Field(
        default=None,
        description="Determines the lease scavenging time value. When this field is set, the appliance permanently deletes the free and backup leases, that remain in the database beyond a specified period of time. To disable lease scavenging, set the parameter to -1. The minimum positive value must be greater than 86400 seconds (1 day).",
    )
    log_lease_events: bool | None = Field(
        default=None,
        description="This value specifies whether the Grid DHCP members log lease events is enabled or not.",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the Infoblox Grid. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )
    low_water_mark: int | None = Field(
        default=None,
        description="Determines the low watermark value. If the percent of allocated addresses drops below this watermark, the appliance makes a syslog entry and if enabled, sends an e-mail notification.",
    )
    low_water_mark_reset: int | None = Field(
        default=None,
        description="Determines the low watermark reset value.If the percentage of allocated addresses exceeds this value, a corresponding SNMP trap is reset. A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The low watermark reset value must be higher than the low watermark value.",
    )
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
    ) = Field(
        default=None,
        description="The Microsoft client DHCP IPv4 code page value of a Grid. This value is the hostname translation code page for Microsoft DHCP IPv4 clients.",
    )
    nextserver: str | None = Field(
        default=None,
        description="The next server value of a DHCP server. This value is the IP address or name of the boot file server on which the boot file is stored.",
    )
    option60_match_rules: list[dict[str, Any]] | None = Field(
        default=None, description="The list of option 60 match rules."
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object. Note that WAPI does not return special options 'routers', 'domain-name-servers', 'domain-name' and 'broadcast-address' with empty values for this object.",
    )
    ping_count: int | None = Field(
        default=None,
        description="Specifies the number of pings that the Infoblox appliance sends to an IP address to verify that it is not in use. Values are range is from 0 to 10, where 0 disables pings.",
    )
    ping_timeout: int | None = Field(
        default=None,
        description="Indicates the number of milliseconds the appliance waits for a response to its ping. Valid values are 100, 500, 1000, 2000, 3000, 4000 and 5000 milliseconds.",
    )
    preferred_lifetime: int | None = Field(
        default=None, description="The preferred lifetime value."
    )
    prefix_length_mode: Literal["EXACT", "IGNORE", "MINIMUM", "MAXIMUM", "PREFER"] | str | None = (
        Field(default=None, description="The Prefix length mode for DHCPv6.")
    )
    protocol_hostname_rewrite_policies: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of hostname rewrite policies."
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="Specifies the duration of time it takes a host to connect to a boot server, such as a TFTP server, and download the file it needs to boot. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    recycle_leases: bool | None = Field(
        default=None,
        description="Determines if the recycle leases feature is enabled or not. If you enabled this feature, and then delete a DHCP range, the appliance stores active leases from this range up to one week after the leases expires.",
    )
    restart_setting: dict[str, Any] | None = Field(
        default=None, description="Settings controlling DNS service restart behavior."
    )
    retry_ddns_updates: bool | None = Field(
        default=None,
        description="Indicates whether the DHCP server makes repeated attempts to send DDNS updates to a DNS server.",
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
    txt_record_handling: (
        Literal["ISC", "ISC_TRANSITIONAL", "IGNORE_CONTENTS", "MS"] | str | None
    ) = Field(
        default=None,
        description="The Grid-level TXT record handling value. This value specifies how DHCP should treat the TXT records when performing DNS updates.",
    )
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="Controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_lifetime: int | None = Field(
        default=None, description="The valid lifetime for the Grid members."
    )
