# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridDns - NIOS Grid DNS properties.

All properties from ``components.schemas.GridDns`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class GridDns(BaseModel):
    """NIOS Grid DNS properties."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    add_client_ip_mac_options: bool | None = Field(
        default=None,
        description="Add custom IP, MAC and DNS View name ENDS0 options to outgoing recursive queries.",
    )
    allow_bulkhost_ddns: Literal["REFUSAL", "SUCCESS"] | str | None = Field(
        default=None, description="Determines if DDNS bulk host is allowed or not."
    )
    allow_gss_tsig_zone_updates: bool | None = Field(
        default=None,
        description="Determines whether GSS-TSIG zone update is enabled for all Grid members.",
    )
    allow_query: list[dict[str, Any]] | None = Field(
        default=None,
        description="Determines if queries from the specified IPv4 or IPv6 addresses and networks are allowed or not. The appliance can also use Transaction Signature (TSIG) keys to authenticate the queries.",
    )
    allow_recursive_query: bool | None = Field(
        default=None,
        description="Determines if the responses to recursive queries are enabled or not.",
    )
    allow_transfer: list[dict[str, Any]] | None = Field(
        default=None,
        description="Determines if zone transfers from specified IPv4 or IPv6 addresses and networks or transfers from hosts authenticated by Transaction signature (TSIG) key are allowed or not.",
    )
    allow_update: list[dict[str, Any]] | None = Field(
        default=None,
        description="Determines if dynamic updates from specified IPv4 or IPv6 addresses, networks or from host authenticated by TSIG key are allowed or not.",
    )
    anonymize_response_logging: bool | None = Field(
        default=None,
        description="Determines if the anonymization of captured DNS responses is enabled or disabled.",
    )
    attack_mitigation: dict[str, Any] | None = Field(
        default=None, description="DNS attack-mitigation (RRL/anti-spoof) settings."
    )
    auto_blackhole: dict[str, Any] | None = Field(
        default=None, description="Settings controlling automatic blackholing of DNS clients."
    )
    bind_check_names_policy: Literal["FAIL", "WARN"] | str | None = Field(
        default=None,
        description='The BIND check names policy, which indicates the action the appliance takes when it encounters host names that do not comply with the Strict Hostname Checking policy. This method applies only if the host name restriction policy is set to "Strict Hostname Checking".',
    )
    bind_hostname_directive: Literal["NONE", "HOSTNAME"] | str | None = Field(
        default=None, description="The value of the hostname directive for BIND."
    )
    blackhole_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of IPv4 or IPv6 addresses and networks from which DNS queries are blocked.",
    )
    blacklist_action: Literal["REDIRECT", "REFUSE"] | str | None = Field(
        default=None,
        description="The action to perform when a domain name matches the pattern defined in a rule that is specified by the blacklist ruleset.",
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
        description="The TTL value (in seconds) of the synthetic DNS responses that result from blacklist redirection.",
    )
    blacklist_rulesets: list[str] | None = Field(
        default=None,
        description="The DNS Ruleset object names assigned at the Grid level for blacklist redirection.",
    )
    bulk_host_name_templates: list[dict[str, Any] | str] | None = Field(
        default=None,
        description='The list of bulk host name templates. There are four Infoblox predefined bulk host name templates. Template Name Template Format "Four Octets" -$1-$2-$3-$4 "Three Octets" -$2-$3-$4 "Two Octets" -$3-$4 "One Octet" -$4',
    )
    capture_dns_queries_on_all_domains: bool | None = Field(
        default=None,
        description="Determines if the capture of DNS queries for all domains is enabled or disabled.",
    )
    check_names_for_ddns_and_zone_transfer: bool | None = Field(
        default=None,
        description="Determines whether the application of BIND check-names for zone transfers and DDNS updates are enabled.",
    )
    client_subnet_domains: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of zone domain names that are allowed or forbidden for EDNS client subnet (ECS) recursion.",
    )
    client_subnet_ipv4_prefix_length: int | None = Field(
        default=None,
        description="Default IPv4 Source Prefix-Length used when sending queries with EDNS client subnet option.",
    )
    client_subnet_ipv6_prefix_length: int | None = Field(
        default=None,
        description="Default IPv6 Source Prefix-Length used when sending queries with EDNS client subnet option.",
    )
    copy_client_ip_mac_options: bool | None = Field(
        default=None,
        description="Copy custom IP, MAC and DNS View name ENDS0 options from incoming to outgoing recursive queries.",
    )
    copy_xfer_to_notify: bool | None = Field(
        default=None,
        description="The allowed IPs, from the zone transfer list, added to the also-notify statement in the named.conf file.",
    )
    custom_root_name_servers: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of customized root nameserver(s). You can use Internet root name servers or specify host names and IP addresses of custom root name servers.",
    )
    ddns_force_creation_timestamp_update: bool | None = Field(
        default=None,
        description="Defines whether creation timestamp of RR should be updated ' when DDNS update happens even if there is no change to ' the RR.",
    )
    ddns_principal_group: str | None = Field(
        default=None, description="The DDNS Principal cluster group name."
    )
    ddns_principal_tracking: bool | None = Field(
        default=None, description="Determines if the DDNS principal track is enabled or disabled."
    )
    ddns_restrict_patterns: bool | None = Field(
        default=None,
        description="Determines if an option to restrict DDNS update request based on FQDN patterns is enabled or disabled.",
    )
    ddns_restrict_patterns_list: list[str] | None = Field(
        default=None,
        description="The unordered list of restriction patterns for an option of to restrict DDNS updates based on FQDN patterns.",
    )
    ddns_restrict_protected: bool | None = Field(
        default=None,
        description="Determines if an option to restrict DDNS update request to protected resource records is enabled or disabled.",
    )
    ddns_restrict_secure: bool | None = Field(
        default=None,
        description="Determines if DDNS update request for principal other than target resource record's principal is restricted.",
    )
    ddns_restrict_static: bool | None = Field(
        default=None,
        description="Determines if an option to restrict DDNS update request to resource records which are marked as 'STATIC' is enabled or disabled.",
    )
    default_bulk_host_name_template: str | None = Field(
        default=None, description="Default bulk host name of a Grid DNS."
    )
    default_ttl: int | None = Field(
        default=None,
        description="The default TTL value of a Grid DNS object. This interval tells the secondary how long the data can be cached.",
    )
    disable_edns: bool | None = Field(
        default=None,
        description="Determines if the EDNS0 support for queries that require recursive resolution on Grid members is enabled or not.",
    )
    dns64_groups: list[str] | None = Field(
        default=None,
        description="The list of DNS64 synthesis groups associated with this Grid DNS object.",
    )
    dns_cache_acceleration_ttl: int | None = Field(
        default=None,
        description="The minimum TTL value, in seconds, that a DNS record must have in order for it to be cached by the DNS Cache Acceleration service. An integer from 1 to 65000 that represents the TTL in seconds.",
    )
    dns_health_check_anycast_control: bool | None = Field(
        default=None,
        description="Determines if the anycast failure (BFD session down) is enabled on member failure or not.",
    )
    dns_health_check_domain_list: list[str] | None = Field(
        default=None, description="The list of domain names for the DNS health check."
    )
    dns_health_check_interval: int | None = Field(
        default=None, description="The time interval (in seconds) for DNS health check."
    )
    dns_health_check_recursion_flag: bool | None = Field(
        default=None, description="Determines if the recursive DNS health check is enabled or not."
    )
    dns_health_check_retries: int | None = Field(
        default=None, description="The number of DNS health check retries."
    )
    dns_health_check_timeout: int | None = Field(
        default=None, description="The DNS health check timeout interval (in seconds)."
    )
    dns_query_capture_file_time_limit: int | None = Field(
        default=None, description="The time limit (in minutes) for the DNS query capture file."
    )
    dnssec_blacklist_enabled: bool | None = Field(
        default=None,
        description="Determines if the blacklist rules for DNSSEC-enabled clients are enabled or not.",
    )
    dnssec_dns64_enabled: bool | None = Field(
        default=None,
        description="Determines if the DNS64 groups for DNSSEC-enabled clients are enabled or not.",
    )
    dnssec_enabled: bool | None = Field(
        default=None, description="Determines if the DNS security extension is enabled or not."
    )
    dnssec_expired_signatures_enabled: bool | None = Field(
        default=None, description="Determines when the DNS member accepts expired signatures."
    )
    dnssec_key_params: dict[str, Any] | None = Field(
        default=None, description="DNSSEC key generation parameters."
    )
    dnssec_negative_trust_anchors: list[str] | None = Field(
        default=None,
        description="A list of zones for which the server does not perform DNSSEC validation.",
    )
    dnssec_nxdomain_enabled: bool | None = Field(
        default=None,
        description="Determines if the NXDOMAIN rules for DNSSEC-enabled clients are enabled or not.",
    )
    dnssec_rpz_enabled: bool | None = Field(
        default=None,
        description="Determines if the RPZ policies for DNSSEC-enabled clients are enabled or not.",
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
    dtc_dns_queries_specific_behavior: (
        Literal["DTC_RESPONSE_ANYWAY", "DNS_RESPONSE_IF_NO_DTC", "DROP_LBDN_MATCHED_QUERY"]
        | str
        | None
    ) = Field(
        default=None,
        description="Setting to control specific behavior for DTC DNS responses for incoming lbdn matched queries.",
    )
    dtc_dnssec_mode: Literal["SIGNED", "UNSIGNED"] | str | None = Field(
        default=None, description="DTC DNSSEC operation mode."
    )
    dtc_edns_prefer_client_subnet: bool | None = Field(
        default=None,
        description="Determines whether to prefer the client address from the edns-client-subnet option for DTC or not.",
    )
    dtc_scheduled_backup: dict[str, Any] | None = Field(default=None)
    dtc_topology_ea_list: list[str] | None = Field(
        default=None,
        description='The DTC topology extensible attribute definition list. When configuring a DTC topology, users may configure classification as either "Geographic" or "Extensible Attributes". Selecting extensible attributes will replace supported Topology database labels (Continent, Country, Subdivision, City) with the names of the selection EA types and provide values extracted from DHCP Network Container, Network and Range objects with those extensible attributes.',
    )
    edns_udp_size: int | None = Field(
        default=None,
        description="Advertises the EDNS0 buffer size to the upstream server. The value should be between 512 and 4096 bytes. The recommended value is between 512 and 1220 bytes.",
    )
    email: str | None = Field(default=None, description="The email address of a Grid DNS object.")
    enable_blackhole: bool | None = Field(
        default=None, description="Determines if the blocking of DNS queries is enabled or not."
    )
    enable_blacklist: bool | None = Field(
        default=None, description="Determines if a blacklist is enabled or not."
    )
    enable_capture_dns_queries: bool | None = Field(
        default=None,
        description="Determines if the capture of DNS queries is enabled or disabled.",
    )
    enable_capture_dns_responses: bool | None = Field(
        default=None,
        description="Determines if the capture of DNS responses is enabled or disabled.",
    )
    enable_client_subnet_forwarding: bool | None = Field(
        default=None,
        description="Determines whether to enable forwarding EDNS client subnet options to upstream servers.",
    )
    enable_client_subnet_recursive: bool | None = Field(
        default=None,
        description="Determines whether to enable adding EDNS client subnet options in recursive resolution. The client_subnet_domains parameter value must not be empty to enable the enable_client_subnet_recursive parameter.",
    )
    enable_delete_associated_ptr: bool | None = Field(
        default=None,
        description="Determines if the ability to automatically remove associated PTR records while deleting A or AAAA records is enabled or not.",
    )
    enable_dns64: bool | None = Field(
        default=None, description="Determines if the DNS64 support is enabled or not."
    )
    enable_dns_health_check: bool | None = Field(
        default=None, description="Determines if the DNS health check is enabled or not."
    )
    enable_dnstap_auth_queries: bool | None = Field(
        default=None, description="Enable DNSTAP for authoritative query messages."
    )
    enable_dnstap_auth_responses: bool | None = Field(
        default=None, description="Enable DNSTAP for authoritative response messages."
    )
    enable_dnstap_client_queries: bool | None = Field(
        default=None, description="Enable DNSTAP for client query messages."
    )
    enable_dnstap_client_responses: bool | None = Field(
        default=None, description="Enable DNSTAP for client response messages."
    )
    enable_dnstap_forwarder_queries: bool | None = Field(
        default=None, description="Enable DNSTAP for forwarder query messages."
    )
    enable_dnstap_forwarder_responses: bool | None = Field(
        default=None, description="Enable DNSTAP for forwarder response messages."
    )
    enable_dnstap_queries: bool | None = Field(
        default=None,
        description="Determines whether the query messages need to be forwarded to DNSTAP or not.",
    )
    enable_dnstap_resolver_queries: bool | None = Field(
        default=None, description="Enable DNSTAP for resolver query messages."
    )
    enable_dnstap_resolver_responses: bool | None = Field(
        default=None, description="Enable DNSTAP for resolver response messages."
    )
    enable_dnstap_responses: bool | None = Field(
        default=None,
        description="Determines whether the response messages need to be forwarded to DNSTAP or not.",
    )
    enable_dnstap_setting: bool | None = Field(
        default=None, description="Indicates whether DNSTAP is enabled."
    )
    enable_dnstap_violations_tls: bool | None = Field(
        default=None,
        description="Determines whether the violations messages need to be forwarded to DNSTAP or not.",
    )
    enable_excluded_domain_names: bool | None = Field(
        default=None,
        description="Determines if excluding domain names from captured DNS queries and responses is enabled or disabled.",
    )
    enable_fixed_rrset_order_fqdns: bool | None = Field(
        default=None, description="Determines if the fixed RRset order FQDN is enabled or not."
    )
    enable_ftc: bool | None = Field(
        default=None, description="Determines whether Fault Tolerant Caching (FTC) is enabled."
    )
    enable_gss_tsig: bool | None = Field(
        default=None,
        description="Determines whether all appliances in the Grid are enabled to receive GSS-TSIG authenticated updates from DNS clients.",
    )
    enable_host_rrset_order: bool | None = Field(
        default=None, description="Determines if the host RRset order is enabled or not."
    )
    enable_hsm_signing: bool | None = Field(
        default=None,
        description="Determines whether Hardware Security Modules (HSMs) are enabled for key generation and signing. Note, that you must configure the HSM group with at least one enabled HSM.",
    )
    enable_notify_source_port: bool | None = Field(
        default=None,
        description="Determines if the notify source port at the Grid Level is enabled or not.",
    )
    enable_query_rewrite: bool | None = Field(
        default=None, description="Determines if the DNS query rewrite is enabled or not."
    )
    enable_query_source_port: bool | None = Field(
        default=None,
        description="Determines if the query source port at the Grid Level is enabled or not.",
    )
    excluded_domain_names: list[str] | None = Field(
        default=None,
        description="The list of domains that are excluded from DNS query and response capture.",
    )
    expire_after: int | None = Field(
        default=None,
        description="The expiration time of a Grid DNS object. If the secondary DNS server fails to contact the primary server for the specified interval, the secondary server stops giving out answers about the zone because the zone data is too old to be useful.",
    )
    file_transfer_setting: dict[str, Any] | None = Field(
        default=None,
        description="File-transfer (FTP/TFTP) settings used for backup/restore and named.conf.",
    )
    filter_aaaa: Literal["YES", "NO", "BREAK_DNSSEC"] | str | None = Field(
        default=None, description="The type of AAAA filtering for this member DNS object."
    )
    filter_aaaa_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of IPv4 addresses and networks from which queries are received. AAAA filtering is applied to these addresses.",
    )
    fixed_rrset_order_fqdns: list[dict[str, Any]] | None = Field(
        default=None,
        description="The fixed RRset order FQDN. If this field does not contain an empty value, the appliance will automatically set the enable_fixed_rrset_order_fqdns field to 'true', unless the same request sets the enable field to 'false'.",
    )
    forward_only: bool | None = Field(
        default=None,
        description='Determines if member sends queries to forwarders only. When the value is "true", the member sends queries to forwarders only, and not to other internal or Internet root servers.',
    )
    forward_updates: bool | None = Field(
        default=None,
        description="Determines if secondary servers is allowed to forward updates to the DNS server or not.",
    )
    forwarders: list[str] | None = Field(
        default=None,
        description="The forwarders for the member. A forwarder is essentially a name server to which other name servers first send all of their off-site queries. The forwarder builds up a cache of information, avoiding the need for the other name servers to send queries off-site.",
    )
    ftc_expired_record_timeout: int | None = Field(
        default=None,
        description="The timeout interval (in seconds) after which the expired Fault Tolerant Caching (FTC)record is stale and no longer valid.",
    )
    ftc_expired_record_ttl: int | None = Field(
        default=None,
        description="The TTL value (in seconds) of the expired Fault Tolerant Caching (FTC) record in DNS responses.",
    )
    gen_eadb_from_hosts: bool | None = Field(
        default=None,
        description="Flag for taking EA values from IPAM Hosts into consideration for the DTC topology EA database.",
    )
    gen_eadb_from_network_containers: bool | None = Field(
        default=None,
        description="Flag for taking EA values from IPAM Network Containers into consideration for the DTC topology EA database.",
    )
    gen_eadb_from_networks: bool | None = Field(
        default=None,
        description="Flag for taking EA values from IPAM Network into consideration for the DTC topology EA database.",
    )
    gen_eadb_from_ranges: bool | None = Field(
        default=None,
        description="Flag for taking EA values from IPAM Ranges into consideration for the DTC topology EA database.",
    )
    gss_tsig_keys: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of GSS-TSIG keys for a Grid DNS object."
    )
    last_queried_acl: list[dict[str, Any]] | None = Field(
        default=None,
        description="Determines last queried ACL for the specified IPv4 or IPv6 addresses and networks in scavenging settings.",
    )
    logging_categories: dict[str, Any] | None = Field(
        default=None, description="Per-category DNS logging settings."
    )
    max_cache_ttl: int | None = Field(
        default=None,
        description="The maximum time (in seconds) for which the server will cache positive answers.",
    )
    max_cached_lifetime: int | None = Field(
        default=None,
        description="The maximum time (in seconds) a DNS response can be stored in the hardware acceleration cache. Valid values are unsigned integer between 60 and 86400, inclusive.",
    )
    max_ncache_ttl: int | None = Field(
        default=None,
        description="The maximum time (in seconds) for which the server will cache negative (NXDOMAIN) responses. The maximum allowed value is 604800.",
    )
    max_udp_size: int | None = Field(
        default=None,
        description="The value is used by authoritative DNS servers to never send DNS responses larger than the configured value. The value should be between 512 and 4096 bytes. The recommended value is between 512 and 1220 bytes.",
    )
    member_secondary_notify: bool | None = Field(
        default=None,
        description="Determines if Grid members that are authoritative secondary servers are allowed to send notification messages to external name servers, if the Grid member that is primary for a zone fails or loses connectivity.",
    )
    negative_ttl: int | None = Field(
        default=None,
        description='The negative TTL value of a Grid DNS object. This interval tells the secondary how long data can be cached for "Does Not Respond" responses.',
    )
    notify_delay: int | None = Field(
        default=None,
        description="Specifies with how many seconds of delay the notify messages are sent to secondaries.",
    )
    notify_source_port: int | None = Field(
        default=None,
        description="The source port for notify messages. When requesting zone transfers from the primary server, some secondary DNS servers use the source port number (the primary server used to send the notify message) as the destination port number in the zone transfer request. Valid values are between 1 and 63999. The default is picked by BIND.",
    )
    nsgroup_default: str | None = Field(default=None, description="The default nameserver group.")
    nsgroups: list[str] | None = Field(
        default=None,
        description="A name server group is a collection of one primary DNS server and one or more secondary DNS servers.",
    )
    nxdomain_log_query: bool | None = Field(
        default=None, description="Determines if NXDOMAIN redirection queries are logged or not."
    )
    nxdomain_redirect: bool | None = Field(
        default=None, description="Determines if NXDOMAIN redirection is enabled or not."
    )
    nxdomain_redirect_addresses: list[str] | None = Field(
        default=None, description="The list of IPv4 NXDOMAIN redirection addresses."
    )
    nxdomain_redirect_addresses_v6: list[str] | None = Field(
        default=None, description="The list of IPv6 NXDOMAIN redirection addresses."
    )
    nxdomain_redirect_ttl: int | None = Field(
        default=None,
        description="The TTL value (in seconds) of synthetic DNS responses that result from NXDOMAIN redirection.",
    )
    nxdomain_rulesets: list[str] | None = Field(
        default=None,
        description="The Ruleset object names assigned at the Grid level for NXDOMAIN redirection.",
    )
    preserve_host_rrset_order_on_secondaries: bool | None = Field(
        default=None,
        description="Determines if the host RRset order on secondaries is preserved or not.",
    )
    protocol_record_name_policies: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of record name policies."
    )
    query_rewrite_domain_names: list[str] | None = Field(
        default=None, description="The list of domain names that trigger DNS query rewrite."
    )
    query_rewrite_prefix: str | None = Field(
        default=None, description="The domain name prefix for DNS query rewrite."
    )
    query_source_port: int | None = Field(
        default=None,
        description="The source port for queries. Specifying a source port number for recursive queries ensures that a firewall will allow the response. Valid values are between 1 and 63999. The default is picked by BIND.",
    )
    recursive_query_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of IPv4 or IPv6 addresses, networks or hosts authenticated by Transaction signature (TSIG) key from which recursive queries are allowed or denied.",
    )
    refresh_timer: int | None = Field(
        default=None,
        description="The refresh time. This interval tells the secondary how often to send a message to the primary for a zone to check that its data is current, and retrieve fresh data if it is not.",
    )
    resolver_query_timeout: int | None = Field(
        default=None, description="The recursive query timeout for the member."
    )
    response_rate_limiting: dict[str, Any] | None = Field(
        default=None, description="Response rate-limiting (RRL) settings."
    )
    restart_setting: dict[str, Any] | None = Field(
        default=None, description="Settings controlling DNS service restart behavior."
    )
    retry_timer: int | None = Field(
        default=None,
        description="The retry time. This interval tells the secondary how long to wait before attempting to recontact the primary after a connection failure occurs between the two servers.",
    )
    root_name_server_type: Literal["CUSTOM", "INTERNET"] | str | None = Field(
        default=None, description="Determines the type of root name servers."
    )
    rpz_disable_nsdname_nsip: bool | None = Field(
        default=None,
        description="Determines if NSDNAME and NSIP resource records from RPZ feeds are enabled or not.",
    )
    rpz_drop_ip_rule_enabled: bool | None = Field(
        default=None,
        description="Enables the appliance to ignore RPZ-IP triggers with prefix lengths less than the specified minimum prefix length.",
    )
    rpz_drop_ip_rule_min_prefix_length_ipv4: int | None = Field(
        default=None,
        description="The minimum prefix length for IPv4 RPZ-IP triggers. The appliance ignores RPZ-IP triggers with prefix lengths less than the specified minimum IPv4 prefix length.",
    )
    rpz_drop_ip_rule_min_prefix_length_ipv6: int | None = Field(
        default=None,
        description="The minimum prefix length for IPv6 RPZ-IP triggers. The appliance ignores RPZ-IP triggers with prefix lengths less than the specified minimum IPv6 prefix length.",
    )
    rpz_qname_wait_recurse: bool | None = Field(
        default=None, description="Determines if recursive RPZ lookups are enabled."
    )
    scavenging_settings: dict[str, Any] | None = Field(
        default=None, description="DNS scavenging settings."
    )
    serial_query_rate: int | None = Field(
        default=None,
        description="The number of maximum concurrent SOA queries per second. Valid values are unsigned integer between 20 and 1000, inclusive.",
    )
    server_id_directive: Literal["NONE", "HOSTNAME"] | str | None = Field(
        default=None, description="The value of the server-id directive for BIND DNS."
    )
    sortlist: list[dict[str, Any]] | None = Field(
        default=None,
        description="A sort list determines the order of addresses in responses made to DNS queries.",
    )
    store_locally: bool | None = Field(
        default=None,
        description="Determines if the storage of query capture reports on the appliance is enabled or disabled.",
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
        description="The syslog facility. This is the location on the syslog server to which you want to sort the DNS logging messages.",
    )
    transfer_excluded_servers: list[str] | None = Field(
        default=None, description="The list of excluded DNS servers during zone transfers."
    )
    transfer_format: Literal["MANY_ANSWERS", "ONE_ANSWER"] | str | None = Field(
        default=None,
        description="The BIND format for a zone transfer. This provides tracking capabilities for single or multiple transfers and their associated servers.",
    )
    transfers_in: int | None = Field(
        default=None,
        description="The number of maximum concurrent transfers for the Grid. Valid values are unsigned integer between 10 and 10000, inclusive.",
    )
    transfers_out: int | None = Field(
        default=None,
        description="The number of maximum outbound concurrent zone transfers. Valid values are unsigned integer between 10 and 10000, inclusive.",
    )
    transfers_per_ns: int | None = Field(
        default=None,
        description="The number of maximum concurrent transfers per member. Valid values are unsigned integer between 2 and 10000, inclusive.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    zone_deletion_double_confirm: bool | None = Field(
        default=None,
        description="Determines if the double confirmation during zone deletion is enabled or not.",
    )
    run_scavenging: object | None = Field(
        default=None, description="Function-call payload for the run-scavenging operation."
    )
