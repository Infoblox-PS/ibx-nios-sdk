# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberDns - NIOS member DNS properties.

Key fields from ``components.schemas.MemberDns`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "dns_cache_acceleration_status",
        "host_name",
        "ipv4addr",
        "ipv6addr",
        "uuid",
    }
)


class MemberDns(BaseModel):
    """NIOS member DNS properties."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    add_client_ip_mac_options: bool | None = Field(
        default=None,
        description="Add custom IP, MAC and DNS View name ENDS0 options to outgoing recursive queries.",
    )
    additional_ip_list: list[str] | None = Field(
        default=None,
        description='The list of additional IP addresses on which DNS is enabled for a Grid member. Only one of "additional_ip_list" or "additional_ip_list_struct" should be set when modifying the object.',
    )
    additional_ip_list_struct: list[dict[str, Any]] | None = Field(
        default=None,
        description='The list of additional IP addresses and IP Space Discriminator short names on which DNS is enabled for a Grid member. Only one of "additional_ip_list" or "additional_ip_list_struct" should be set when modifying the object.',
    )
    allow_gss_tsig_zone_updates: bool | None = Field(
        default=None,
        description="Determines whether the GSS-TSIG zone updates is enabled for the Grid member.",
    )
    allow_query: list[dict[str, Any]] | None = Field(
        default=None,
        description="Determines if queries from specified IPv4 or IPv6 addresses and networks are enabled or not. The appliance can also use Transaction Signature (TSIG) keys to authenticate the queries. This setting overrides the Grid query settings.",
    )
    allow_recursive_query: bool | None = Field(
        default=None,
        description="Determines if the responses to recursive queries is enabled or not. This setting overrides Grid recursive query settings.",
    )
    allow_transfer: list[dict[str, Any]] | None = Field(
        default=None,
        description="Allows or rejects zone transfers from specified IPv4 or IPv6 addresses and networks or allows transfers from hosts authenticated by Transaction signature (TSIG) key. This setting overrides the Grid zone transfer settings.",
    )
    allow_update: list[dict[str, Any]] | None = Field(
        default=None,
        description="Allows or rejects dynamic updates from specified IPv4 or IPv6 addresses, networks or from host authenticated by TSIG key. This setting overrides Grid update settings.",
    )
    anonymize_response_logging: bool | None = Field(
        default=None,
        description="The flag that indicates whether the anonymization of captured DNS responses is enabled or disabled.",
    )
    attack_mitigation: dict[str, Any] | None = Field(
        default=None, description="DNS attack-mitigation (RRL/anti-spoof) settings."
    )
    auto_blackhole: dict[str, Any] | None = Field(
        default=None, description="Settings controlling automatic blackholing of DNS clients."
    )
    bind_check_names_policy: Literal["FAIL", "WARN"] | str | None = Field(
        default=None,
        description="The BIND check names policy, which indicates the action the appliance takes when it encounters host names that do not comply with the Strict Hostname Checking policy. This method applies only if the host name restriction policy is set to 'Strict Hostname Checking'.",
    )
    bind_hostname_directive: Literal["NONE", "HOSTNAME", "USER_DEFINED"] | str | None = Field(
        default=None, description="The value of the hostname directive for BIND."
    )
    blackhole_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of IPv4 or IPv6 addresses and networks from which DNS queries are blocked. This setting overrides the Grid blackhole_list.",
    )
    blacklist_action: Literal["REDIRECT", "REFUSE"] | str | None = Field(
        default=None,
        description="The action to perform when a domain name matches the pattern defined in a rule that is specified by the blacklist_ruleset method.",
    )
    blacklist_log_query: bool | None = Field(
        default=None, description="Determines if blacklist redirection queries are logged or not."
    )
    blacklist_redirect_addresses: list[str] | None = Field(
        default=None,
        description="The IP addresses the appliance includes in the response it sends in place of a blacklisted IP address.",
    )
    blacklist_redirect_ttl: int | None = Field(
        default=None,
        description="The TTL value of the synthetic DNS responses that result from blacklist redirection.",
    )
    blacklist_rulesets: list[str] | None = Field(
        default=None,
        description="The DNS Ruleset object names assigned at the Grid level for blacklist redirection.",
    )
    capture_dns_queries_on_all_domains: bool | None = Field(
        default=None,
        description="The flag that indicates whether the capture of DNS queries for all domains is enabled or disabled.",
    )
    copy_client_ip_mac_options: bool | None = Field(
        default=None,
        description="Copy custom IP, MAC and DNS View name ENDS0 options from incoming to outgoing recursive queries.",
    )
    copy_xfer_to_notify: bool | None = Field(
        default=None,
        description="Copies the allowed IPs from the zone transfer list into the also-notify statement in the named.conf file.",
    )
    custom_root_name_servers: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of custom root name servers. You can either select and use Internet root name servers or specify custom root name servers by providing a host name and IP address to which the Infoblox appliance can send queries.",
    )
    disable_edns: bool | None = Field(
        default=None,
        description="The EDNS0 support for queries that require recursive resolution on Grid members.",
    )
    dns64_groups: list[str] | None = Field(
        default=None, description="The list of DNS64 synthesis groups associated with this member."
    )
    dns_cache_acceleration_status: str | None = Field(
        default=None, description="The DNS cache acceleration status."
    )
    dns_cache_acceleration_ttl: int | None = Field(
        default=None,
        description="The minimum TTL value, in seconds, that a DNS record must have in order for it to be cached by the DNS Cache Acceleration service. An integer from 1 to 65000 that represents the TTL in seconds.",
    )
    dnssec_enabled: bool | None = Field(
        default=None, description="Determines if the DNS security extension is enabled or not."
    )
    dnssec_trusted_keys: list[dict[str, Any]] | None = Field(
        default=None, description="The list of trusted keys for the DNSSEC feature."
    )
    dnssec_validation_enabled: bool | None = Field(
        default=None, description="Determines if the DNS security validation is enabled or not."
    )
    dnstap_setting: dict[str, Any] | None = Field(
        default=None, description="dnstap logging settings."
    )
    domains_to_capture_dns_queries: list[str] | None = Field(
        default=None, description="The list of domains for DNS query capture."
    )
    edns_udp_size: int | None = Field(
        default=None,
        description="Advertises the EDNS0 buffer size to the upstream server. The value should be between 512 and 4096 bytes. The recommended value is between 512 and 1220 bytes.",
    )
    enable_blackhole: bool | None = Field(
        default=None,
        description="Determines if the blocking of DNS queries is enabled or not. This setting overrides the Grid enable_blackhole settings.",
    )
    enable_blacklist: bool | None = Field(
        default=None, description="Determines if a blacklist is enabled or not on the Grid member."
    )
    enable_capture_dns_queries: bool | None = Field(
        default=None,
        description="The flag that indicates whether the capture of DNS queries is enabled or disabled.",
    )
    enable_capture_dns_responses: bool | None = Field(
        default=None,
        description="The flag that indicates whether the capture of DNS responses is enabled or disabled.",
    )
    enable_dns64: bool | None = Field(
        default=None,
        description="Determines if the DNS64 support is enabled or not for this member.",
    )
    enable_gss_tsig: bool | None = Field(
        default=None,
        description="Determines whether the appliance is enabled to receive GSS-TSIG authenticated updates from DHCP clients.",
    )
    enable_query_rewrite: bool | None = Field(
        default=None,
        description="Determines if the DNS query rewrite is enabled or not for this member.",
    )
    filter_aaaa: Literal["YES", "NO", "BREAK_DNSSEC"] | str | None = Field(
        default=None, description="The type of AAAA filtering for this member DNS object."
    )
    filter_aaaa_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of IPv4 addresses and networks from which queries are received. AAAA filtering is applied to these addresses.",
    )
    forward_only: bool | None = Field(
        default=None,
        description='Permits this member to send queries to forwarders only. When the value is "true", the member sends queries to forwarders only, and not to other internal or Internet root servers.',
    )
    forward_updates: bool | None = Field(
        default=None,
        description="Allows secondary servers to forward updates to the DNS server. This setting overrides grid update settings.",
    )
    forwarders: list[str] | None = Field(
        default=None,
        description="The forwarders for the member. A forwarder is essentially a name server to which other name servers first send all of their off-site queries. The forwarder builds up a cache of information, avoiding the need for the other name servers to send queries off-site. This setting overrides the Grid level setting.",
    )
    gss_tsig_keys: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of GSS-TSIG keys for a member DNS object."
    )
    host_name: str | None = Field(default=None, description="The host name of the Grid member.")
    ipv4addr: str | None = Field(default=None, description="The IPv4 Address of the Grid member.")
    ipv6addr: str | None = Field(default=None, description="The IPv6 Address of the Grid member.")
    logging_categories: dict[str, Any] | None = Field(
        default=None, description="Per-category DNS logging settings."
    )
    max_cache_ttl: int | None = Field(
        default=None,
        description="The maximum time (in seconds) for which the server will cache positive answers.",
    )
    max_ncache_ttl: int | None = Field(
        default=None,
        description="The maximum time (in seconds) for which the server will cache negative (NXDOMAIN) responses. The maximum allowed value is 604800.",
    )
    max_udp_size: int | None = Field(
        default=None,
        description="The value is used by authoritative DNS servers to never send DNS responses larger than the configured value. The value should be between 512 and 4096 bytes. The recommended value is between 512 and 1220 bytes.",
    )
    notify_delay: int | None = Field(
        default=None,
        description="Specifies the number of seconds of delay the notify messages are sent to secondaries.",
    )
    nxdomain_log_query: bool | None = Field(
        default=None, description="Determines if NXDOMAIN redirection queries are logged or not."
    )
    nxdomain_redirect: bool | None = Field(
        default=None, description="Enables NXDOMAIN redirection."
    )
    nxdomain_redirect_addresses: list[str] | None = Field(
        default=None, description="The IPv4 NXDOMAIN redirection addresses."
    )
    nxdomain_redirect_ttl: int | None = Field(
        default=None,
        description="The TTL value of synthetic DNS responses that result from NXDOMAIN redirection.",
    )
    nxdomain_rulesets: list[str] | None = Field(
        default=None,
        description="The names of the Ruleset objects assigned at the Grid level for NXDOMAIN redirection.",
    )
    recursive_query_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of IPv4 or IPv6 addresses, networks or hosts authenticated by Transaction signature (TSIG) key from which recursive queries are allowed or denied.",
    )
    resolver_query_timeout: int | None = Field(
        default=None,
        description="The recursive query timeout for the member. The value must be 0 or between 10 and 30.",
    )
    response_rate_limiting: dict[str, Any] | None = Field(
        default=None, description="Response rate-limiting (RRL) settings."
    )
    root_name_server_type: Literal["CUSTOM", "INTERNET"] | str | None = Field(
        default=None, description="Determines the type of root name servers."
    )
    rpz_disable_nsdname_nsip: bool | None = Field(
        default=None,
        description="Enables NSDNAME and NSIP resource records from RPZ feeds at member level.",
    )
    rpz_drop_ip_rule_enabled: bool | None = Field(
        default=None,
        description="Enables the appliance to ignore RPZ-IP triggers with prefix lengths less than the specified minimum prefix length.",
    )
    rpz_qname_wait_recurse: bool | None = Field(
        default=None,
        description="The flag that indicates whether recursive RPZ lookups are enabled.",
    )
    serial_query_rate: int | None = Field(
        default=None,
        description="The number of maximum concurrent SOA queries per second for the member.",
    )
    sortlist: list[dict[str, Any]] | None = Field(
        default=None,
        description="A sort list determines the order of addresses in responses made to DNS queries. This setting overrides Grid sort list settings.",
    )
    transfer_format: Literal["MANY_ANSWERS", "ONE_ANSWER"] | str | None = Field(
        default=None,
        description="The BIND format for a zone transfer. This provides tracking capabilities for single or multiple transfers and their associated servers.",
    )
    transfers_in: int | None = Field(
        default=None, description="The number of maximum concurrent transfers for the member."
    )
    transfers_out: int | None = Field(
        default=None,
        description="The number of maximum outbound concurrent zone transfers for the member.",
    )
    transfers_per_ns: int | None = Field(
        default=None,
        description="The number of maximum concurrent transfers per member for the member.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    atc_fwd_enable: bool | None = Field(default=None)
    auto_create_a_and_ptr_for_lan2: bool | None = Field(default=None)
    auto_create_aaaa_and_ipv6ptr_for_lan2: bool | None = Field(default=None)
    auto_sort_views: bool | None = Field(default=None)
    bind_hostname_directive_fqdn: str | None = Field(default=None)
    check_names_for_ddns_and_zone_transfer: bool | None = Field(default=None)
    clear_dns_cache: object | None = Field(default=None)
    dns_health_check_anycast_control: bool | None = Field(default=None)
    dns_health_check_domain_list: list[str] | None = Field(default=None)
    dns_health_check_interval: int | None = Field(default=None)
    dns_health_check_recursion_flag: bool | None = Field(default=None)
    dns_health_check_retries: int | None = Field(default=None)
    dns_health_check_timeout: int | None = Field(default=None)
    dns_notify_transfer_source: Literal["VIP", "MGMT", "LAN2", "ANY", "IP"] | str | None = Field(
        default=None
    )
    dns_notify_transfer_source_address: str | None = Field(default=None)
    dns_over_https_endpoint: str | None = Field(default=None)
    dns_over_https_stream_per_connection: int | None = Field(default=None)
    dns_over_tls_service: bool | None = Field(default=None)
    dns_query_capture_file_time_limit: int | None = Field(default=None)
    dns_query_source_address: str | None = Field(default=None)
    dns_query_source_interface: Literal["VIP", "MGMT", "LAN2", "ANY", "IP"] | str | None = Field(
        default=None
    )
    dns_view_address_settings: list[dict[str, Any]] | None = Field(default=None)
    dnssec_blacklist_enabled: bool | None = Field(default=None)
    dnssec_dns64_enabled: bool | None = Field(default=None)
    dnssec_expired_signatures_enabled: bool | None = Field(default=None)
    dnssec_negative_trust_anchors: list[str] | None = Field(default=None)
    dnssec_nxdomain_enabled: bool | None = Field(default=None)
    dnssec_rpz_enabled: bool | None = Field(default=None)
    dnstap_identity: str | None = Field(default=None)
    doh_https_session_duration: int | None = Field(default=None)
    doh_service: bool | None = Field(default=None)
    dtc_dns_queries_specific_behavior: (
        Literal["DTC_RESPONSE_ANYWAY", "DNS_RESPONSE_IF_NO_DTC", "DROP_LBDN_MATCHED_QUERY"]
        | str
        | None
    ) = Field(default=None)
    dtc_edns_prefer_client_subnet: bool | None = Field(default=None)
    dtc_health_source: Literal["VIP", "MGMT", "LAN2", "ANY", "IP"] | str | None = Field(
        default=None
    )
    dtc_health_source_address: str | None = Field(default=None)
    enable_dns: bool | None = Field(default=None)
    enable_dns_cache_acceleration: bool | None = Field(default=None)
    enable_dns_health_check: bool | None = Field(default=None)
    enable_dnstap_auth_queries: bool | None = Field(default=None)
    enable_dnstap_auth_responses: bool | None = Field(default=None)
    enable_dnstap_client_queries: bool | None = Field(default=None)
    enable_dnstap_client_responses: bool | None = Field(default=None)
    enable_dnstap_forwarder_queries: bool | None = Field(default=None)
    enable_dnstap_forwarder_responses: bool | None = Field(default=None)
    enable_dnstap_logging_type: bool | None = Field(default=None)
    enable_dnstap_queries: bool | None = Field(default=None)
    enable_dnstap_resolver_queries: bool | None = Field(default=None)
    enable_dnstap_resolver_responses: bool | None = Field(default=None)
    enable_dnstap_responses: bool | None = Field(default=None)
    enable_dnstap_setting: bool | None = Field(default=None)
    enable_dnstap_violations_tls: bool | None = Field(default=None)
    enable_excluded_domain_names: bool | None = Field(default=None)
    enable_fixed_rrset_order_fqdns: bool | None = Field(default=None)
    enable_ftc: bool | None = Field(default=None)
    enable_notify_source_port: bool | None = Field(default=None)
    enable_query_source_port: bool | None = Field(default=None)
    excluded_domain_names: list[str] | None = Field(default=None)
    extattrs: object | None = Field(
        default=None, description="Extensible attributes (key/value tags) attached to the object."
    )
    file_transfer_setting: object | None = Field(
        default=None,
        description="File-transfer (FTP/TFTP) settings used for backup/restore and named.conf.",
    )
    fixed_rrset_order_fqdns: list[dict[str, Any]] | None = Field(default=None)
    ftc_expired_record_timeout: int | None = Field(default=None)
    ftc_expired_record_ttl: int | None = Field(default=None)
    glue_record_addresses: list[dict[str, Any]] | None = Field(default=None)
    ipv6_glue_record_addresses: list[dict[str, Any]] | None = Field(default=None)
    max_cached_lifetime: int | None = Field(default=None)
    minimal_resp: bool | None = Field(default=None)
    notify_source_port: int | None = Field(default=None)
    nxdomain_redirect_addresses_v6: list[str] | None = Field(default=None)
    query_source_port: int | None = Field(default=None)
    record_name_policy: str | None = Field(default=None)
    recursive_client_limit: int | None = Field(default=None)
    recursive_resolver: Literal["BIND"] | str | None = Field(default=None)
    rpz_drop_ip_rule_min_prefix_length_ipv4: int | None = Field(default=None)
    rpz_drop_ip_rule_min_prefix_length_ipv6: int | None = Field(default=None)
    server_id_directive: Literal["NONE", "HOSTNAME", "USER_DEFINED"] | str | None = Field(
        default=None
    )
    server_id_directive_string: str | None = Field(default=None)
    skip_in_grid_rpz_queries: bool | None = Field(default=None)
    store_locally: bool | None = Field(default=None)
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
    ) = Field(default=None)
    tcp_idle_timeout: int | None = Field(default=None)
    tls_session_duration: int | None = Field(default=None)
    transfer_excluded_servers: list[str] | None = Field(default=None)
    upstream_address_family_preference: Literal["IPV4", "IPV6", "ANY"] | str | None = Field(
        default=None
    )
    use_add_client_ip_mac_options: bool | None = Field(default=None)
    use_allow_query: bool | None = Field(default=None)
    use_allow_transfer: bool | None = Field(default=None)
    use_attack_mitigation: bool | None = Field(default=None)
    use_auto_blackhole: bool | None = Field(default=None)
    use_bind_hostname_directive: bool | None = Field(default=None)
    use_blackhole: bool | None = Field(default=None)
    use_blacklist: bool | None = Field(default=None)
    use_capture_dns_queries_on_all_domains: bool | None = Field(default=None)
    use_copy_client_ip_mac_options: bool | None = Field(default=None)
    use_copy_xfer_to_notify: bool | None = Field(default=None)
    use_disable_edns: bool | None = Field(default=None)
    use_dns64: bool | None = Field(default=None)
    use_dns_cache_acceleration_ttl: bool | None = Field(default=None)
    use_dns_health_check: bool | None = Field(default=None)
    use_dnssec: bool | None = Field(default=None)
    use_dnstap_setting: bool | None = Field(default=None)
    use_dtc_dns_queries_specific_behavior: bool | None = Field(default=None)
    use_dtc_edns_prefer_client_subnet: bool | None = Field(default=None)
    use_edns_udp_size: bool | None = Field(default=None)
    use_enable_capture_dns: bool | None = Field(default=None)
    use_enable_excluded_domain_names: bool | None = Field(default=None)
    use_enable_gss_tsig: bool | None = Field(
        default=None, description="Override flag controlling whether GSS-TSIG is enabled."
    )
    use_enable_query_rewrite: bool | None = Field(default=None)
    use_filter_aaaa: bool | None = Field(default=None)
    use_fixed_rrset_order_fqdns: bool | None = Field(default=None)
    use_forward_updates: bool | None = Field(default=None)
    use_forwarders: bool | None = Field(default=None)
    use_ftc: bool | None = Field(default=None)
    use_gss_tsig_keys: bool | None = Field(
        default=None, description="Override flag controlling whether GSS-TSIG keys are honored."
    )
    use_lan2_ipv6_port: bool | None = Field(default=None)
    use_lan2_port: bool | None = Field(default=None)
    use_lan_ipv6_port: bool | None = Field(default=None)
    use_lan_port: bool | None = Field(default=None)
    use_logging_categories: bool | None = Field(default=None)
    use_max_cache_ttl: bool | None = Field(default=None)
    use_max_cached_lifetime: bool | None = Field(default=None)
    use_max_ncache_ttl: bool | None = Field(default=None)
    use_max_udp_size: bool | None = Field(default=None)
    use_mgmt_ipv6_port: bool | None = Field(default=None)
    use_mgmt_port: bool | None = Field(default=None)
    use_notify_delay: bool | None = Field(default=None)
    use_nxdomain_redirect: bool | None = Field(default=None)
    use_record_name_policy: bool | None = Field(default=None)
    use_recursive_client_limit: bool | None = Field(default=None)
    use_recursive_query_setting: bool | None = Field(default=None)
    use_resolver_query_timeout: bool | None = Field(default=None)
    use_response_rate_limiting: bool | None = Field(default=None)
    use_root_name_server: bool | None = Field(default=None)
    use_root_server_for_all_views: bool | None = Field(default=None)
    use_rpz_disable_nsdname_nsip: bool | None = Field(default=None)
    use_rpz_drop_ip_rule: bool | None = Field(default=None)
    use_rpz_qname_wait_recurse: bool | None = Field(default=None)
    use_serial_query_rate: bool | None = Field(default=None)
    use_server_id_directive: bool | None = Field(default=None)
    use_sortlist: bool | None = Field(default=None)
    use_source_ports: bool | None = Field(default=None)
    use_syslog_facility: bool | None = Field(
        default=None,
        description="Override flag controlling whether the configured syslog facility is used.",
    )
    use_transfers_in: bool | None = Field(default=None)
    use_transfers_out: bool | None = Field(default=None)
    use_transfers_per_ns: bool | None = Field(default=None)
    use_update_setting: bool | None = Field(default=None)
    use_zone_transfer_format: bool | None = Field(default=None)
    views: list[str] | None = Field(default=None)
