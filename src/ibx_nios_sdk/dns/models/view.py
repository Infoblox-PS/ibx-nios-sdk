# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""View - NIOS DNS view (resolution/query segmentation).

All 86 properties from ``components.schemas.View`` in the v2.14 DNS swagger
are represented here.  Deeply nested View-only schemas are typed as
``dict[str, Any]``; see ``dns/NOTES.md`` for the approximated-fields list.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import CloudInfo, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# Only ``is_default`` and ``uuid`` are marked readOnly on the top-level View
# schema in the v2.14 swagger.
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "is_default",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# View-only nested types
# ---------------------------------------------------------------------------


class ViewCustomRootNameServers(_DnsNested):
    """Custom root name-server entry (same shape as ExtServer)."""

    address: str | None = Field(
        default=None, description="The source address of a sortlist object."
    )
    name: str | None = Field(default=None, description="Name of the DNS view.")
    shared_with_ms_parent_delegation: bool | None = Field(
        default=None,
        description="This flag represents whether the name server is shared with the parent Microsoft primary zone's delegation server.",
    )
    stealth: bool | None = Field(
        default=None,
        description="Set this flag to hide the NS record for the primary name server from DNS queries.",
    )
    tsig_key: str | None = Field(
        default=None,
        description="A generated TSIG key. If the external primary server is a NIOS appliance running DNS One 2.x code, this can be set to :2xCOMPAT.",
    )
    tsig_key_alg: Literal["HMAC-MD5", "HMAC-SHA256"] | str | None = Field(
        default=None, description="The TSIG key algorithm."
    )
    tsig_key_name: str | None = Field(
        default=None,
        description="The name of the TSIG key. If 2.x TSIG compatibility is used, this is set to 'tsig_xfer' on retrieval, and ignored on insert or update.",
    )
    use_tsig_key_name: bool | None = Field(default=None, description="Use flag for: tsig_key_name")


class ViewDnssecTrustedKeys(_DnsNested):
    """DNSSEC trusted anchor entry."""

    fqdn: str | None = Field(
        default=None, description="The FQDN of the fixed RRset configuration item."
    )
    algorithm: str | None = Field(
        default=None, description="The DNSSEC algorithm used to generate the key."
    )
    key: str | None = Field(default=None, description="The DNSSEC key.")
    secure_entry_point: bool | None = Field(
        default=None,
        description="The secure entry point flag, if set it means this is a KSK configuration.",
    )
    dnssec_must_be_secure: bool | None = Field(
        default=None, description="Responses must be DNSSEC secure for this hierarchy/domain."
    )


class ViewFilterAaaaList(_DnsNested):
    """AAAA filter list entry."""

    address: str | None = Field(
        default=None, description="The source address of a sortlist object."
    )
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )


class ViewFixedRrsetOrderFqdns(_DnsNested):
    """Fixed RRset order FQDN entry."""

    fqdn: str | None = Field(
        default=None, description="The FQDN of the fixed RRset configuration item."
    )
    record_type: Literal["A", "AAAA", "BOTH"] | str | None = Field(
        default=None,
        description="The record type for the specified FQDN in the fixed RRset configuration.",
    )


class ViewLastQueriedAcl(_DnsNested):
    """Last-queried ACL entry."""

    address: str | None = Field(
        default=None, description="The source address of a sortlist object."
    )
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )


class ViewMatchClients(_DnsNested):
    """Match-clients ACL entry."""

    address: str | None = Field(
        default=None, description="The source address of a sortlist object."
    )
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )
    tsig_key: str | None = Field(
        default=None,
        description="A generated TSIG key. If the external primary server is a NIOS appliance running DNS One 2.x code, this can be set to :2xCOMPAT.",
    )
    tsig_key_alg: Literal["HMAC-MD5", "HMAC-SHA256"] | str | None = Field(
        default=None, description="The TSIG key algorithm."
    )
    tsig_key_name: str | None = Field(
        default=None,
        description="The name of the TSIG key. If 2.x TSIG compatibility is used, this is set to 'tsig_xfer' on retrieval, and ignored on insert or update.",
    )
    use_tsig_key_name: bool | None = Field(default=None, description="Use flag for: tsig_key_name")


class ViewMatchDestinations(_DnsNested):
    """Match-destinations ACL entry."""

    address: str | None = Field(
        default=None, description="The source address of a sortlist object."
    )
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )
    tsig_key: str | None = Field(
        default=None,
        description="A generated TSIG key. If the external primary server is a NIOS appliance running DNS One 2.x code, this can be set to :2xCOMPAT.",
    )
    tsig_key_alg: Literal["HMAC-MD5", "HMAC-SHA256"] | str | None = Field(
        default=None, description="The TSIG key algorithm."
    )
    tsig_key_name: str | None = Field(
        default=None,
        description="The name of the TSIG key. If 2.x TSIG compatibility is used, this is set to 'tsig_xfer' on retrieval, and ignored on insert or update.",
    )
    use_tsig_key_name: bool | None = Field(default=None, description="Use flag for: tsig_key_name")


class ViewResponseRateLimiting(_DnsNested):
    """Response rate-limiting settings."""

    enable_rrl: bool | None = Field(
        default=None, description="Determines if the response rate limiting is enabled or not."
    )
    log_only: bool | None = Field(
        default=None,
        description="Determines if logging for response rate limiting without dropping any requests is enabled or not.",
    )
    responses_per_second: int | None = Field(
        default=None, description="The number of responses per client per second."
    )
    window: int | None = Field(
        default=None, description="The time interval in seconds over which responses are tracked."
    )
    slip: int | None = Field(
        default=None,
        description="The response rate limiting slip. Note that if slip is not equal to 0 every n-th rate-limited UDP request is sent a truncated response instead of being dropped.",
    )


class ViewScavengingSettings(_DnsNested):
    """DNS scavenging configuration block.

    The ``scavenging_schedule`` and ``*_expression_list`` sub-fields are typed
    as ``dict[str, Any]`` - see ``dns/NOTES.md`` (View: approximated fields).
    """

    enable_scavenging: bool | None = Field(
        default=None,
        description="This flag indicates if the resource record scavenging is enabled or not.",
    )
    enable_recurrent_scavenging: bool | None = Field(
        default=None,
        description="This flag indicates if the recurrent resource record scavenging is enabled or not.",
    )
    enable_auto_reclamation: bool | None = Field(
        default=None,
        description="This flag indicates if the automatic resource record scavenging is enabled or not.",
    )
    enable_rr_last_queried: bool | None = Field(
        default=None,
        description="This flag indicates if the resource record last queried monitoring in affected zones is enabled or not.",
    )
    enable_zone_last_queried: bool | None = Field(
        default=None,
        description="This flag indicates if the last queried monitoring for affected zones is enabled or not.",
    )
    reclaim_associated_records: bool | None = Field(
        default=None,
        description="This flag indicates if the associated resource record scavenging is enabled or not.",
    )
    scavenging_schedule: dict[str, Any] | None = Field(
        default=None, description="Schedule setting for cloud discovery task."
    )
    expression_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The expression list. The particular record is treated as reclaimable if expression condition evaluates to 'true' for given record if scavenging hasn't been manually disabled on a given resource record.",
    )
    ea_expression_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The extensible attributes expression list. The particular record is treated as reclaimable if extensible attributes expression condition evaluates to 'true' for given record if scavenging hasn't been manually disabled on a given resource record.",
    )


class ViewSortlist(_DnsNested):
    """Sort-list entry."""

    address: str | None = Field(
        default=None, description="The source address of a sortlist object."
    )
    match_list: list[str] | None = Field(
        default=None, description="The match list of a sortlist."
    )  # ---------------------------------------------------------------------------


# Main View model
# ---------------------------------------------------------------------------


class View(BaseModel):
    """NIOS DNS view configuration.

    All 86 swagger properties are present.  ``is_default`` and ``uuid`` are
    read-only (collected in :data:`READONLY_FIELDS`).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    name: str | None = Field(default=None, description="Name of the DNS view.")
    comment: str | None = Field(
        default=None, description="Comment for the DNS view; maximum 64 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines if the DNS view is disabled or not. When this is set to False, the DNS view is enabled.",
    )
    network_view: str | None = Field(
        default=None,
        description="The name of the network view object associated with this DNS view.",
    )  # --- read-only ---
    is_default: bool | None = Field(
        default=None,
        description="The NIOS appliance provides one default DNS view. You can rename the default view and change its settings, but you cannot delete it. There must always be at least one DNS view in the appliance.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- blacklist / RPZ ---
    blacklist_action: Literal["REDIRECT", "REFUSE"] | str | None = Field(
        default=None,
        description='The action to perform when a domain name matches the pattern defined in a rule that is specified by the blacklist_ruleset method. Valid values are "REDIRECT" or "REFUSE". The default value is "REDIRECT".',
    )
    blacklist_log_query: bool | None = Field(
        default=None,
        description='The flag that indicates whether blacklist redirection queries are logged. Specify "true" to enable logging, or "false" to disable it. The default value is "false".',
    )
    blacklist_redirect_addresses: list[str] | None = Field(
        default=None,
        description="The array of IP addresses the appliance includes in the response it sends in place of a blacklisted IP address.",
    )
    blacklist_redirect_ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value of the synthetic DNS responses resulted from blacklist redirection. The TTL value is a 32-bit unsigned integer that represents the TTL in seconds.",
    )
    blacklist_rulesets: list[str] | None = Field(
        default=None,
        description="The name of the Ruleset object assigned at the Grid level for blacklist redirection.",
    )
    enable_blacklist: bool | None = Field(
        default=None, description="Determines if the blacklist in a DNS view is enabled or not."
    )
    use_blacklist: bool | None = Field(
        default=None,
        description="Use flag for: blacklist_action , blacklist_log_query, blacklist_redirect_addresses, blacklist_redirect_ttl, blacklist_rulesets, enable_blacklist",
    )  # --- cloud info ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- custom root name servers ---
    custom_root_name_servers: list[ViewCustomRootNameServers] | None = Field(
        default=None,
        description="The list of customized root name servers. You can either select and use Internet root name servers or specify custom root name servers by providing a host name and IP address to which the Infoblox appliance can send queries. Include the specified parameter to set the attribute value. Omit the parameter to retrieve the attribute value.",
    )
    root_name_server_type: Literal["CUSTOM", "INTERNET"] | str | None = Field(
        default=None, description="Determines the type of root name servers."
    )
    use_root_name_server: bool | None = Field(
        default=None, description="Use flag for: custom_root_name_servers , root_name_server_type"
    )  # --- DDNS ---
    ddns_force_creation_timestamp_update: bool | None = Field(
        default=None,
        description="Defines whether creation timestamp of RR should be updated ' when DDNS update happens even if there is no change to ' the RR.",
    )
    ddns_principal_group: str | None = Field(
        default=None, description="The DDNS Principal cluster group name."
    )
    ddns_principal_tracking: bool | None = Field(
        default=None,
        description="The flag that indicates whether the DDNS principal track is enabled or disabled.",
    )
    ddns_restrict_patterns: bool | None = Field(
        default=None,
        description="The flag that indicates whether an option to restrict DDNS update request based on FQDN patterns is enabled or disabled.",
    )
    ddns_restrict_patterns_list: list[str] | None = Field(
        default=None,
        description="The unordered list of restriction patterns for an option of to restrict DDNS updates based on FQDN patterns.",
    )
    ddns_restrict_protected: bool | None = Field(
        default=None,
        description="The flag that indicates whether an option to restrict DDNS update request to protected resource records is enabled or disabled.",
    )
    ddns_restrict_secure: bool | None = Field(
        default=None,
        description="The flag that indicates whether DDNS update request for principal other than target resource record's principal is restricted.",
    )
    ddns_restrict_static: bool | None = Field(
        default=None,
        description="The flag that indicates whether an option to restrict DDNS update request to resource records which are marked as 'STATIC' is enabled or disabled.",
    )
    use_ddns_force_creation_timestamp_update: bool | None = Field(
        default=None, description="Use flag for: ddns_force_creation_timestamp_update"
    )
    use_ddns_patterns_restriction: bool | None = Field(
        default=None,
        description="Use flag for: ddns_restrict_patterns_list , ddns_restrict_patterns",
    )
    use_ddns_principal_security: bool | None = Field(
        default=None,
        description="Use flag for: ddns_restrict_secure , ddns_principal_tracking, ddns_principal_group",
    )
    use_ddns_restrict_protected: bool | None = Field(
        default=None, description="Use flag for: ddns_restrict_protected"
    )
    use_ddns_restrict_static: bool | None = Field(
        default=None, description="Use flag for: ddns_restrict_static"
    )  # --- DNS64 ---
    dns64_enabled: bool | None = Field(
        default=None, description="Determines if the DNS64 s enabled or not."
    )
    dns64_groups: list[str] | None = Field(
        default=None,
        description="The list of DNS64 synthesis groups associated with this DNS view.",
    )
    use_dns64: bool | None = Field(
        default=None, description="Use flag for: dns64_enabled , dns64_groups"
    )  # --- DNSSEC ---
    dnssec_enabled: bool | None = Field(
        default=None, description="Determines if the DNS security extension is enabled or not."
    )
    dnssec_expired_signatures_enabled: bool | None = Field(
        default=None,
        description="Determines if the DNS security extension accepts expired signatures or not.",
    )
    dnssec_negative_trust_anchors: list[str] | None = Field(
        default=None,
        description="A list of zones for which the server does not perform DNSSEC validation.",
    )
    dnssec_trusted_keys: list[ViewDnssecTrustedKeys] | None = Field(
        default=None, description="The list of trusted keys for the DNS security extension."
    )
    dnssec_validation_enabled: bool | None = Field(
        default=None, description="Determines if the DNS security validation is enabled or not."
    )
    use_dnssec: bool | None = Field(
        default=None,
        description="Use flag for: dnssec_enabled , dnssec_expired_signatures_enabled, dnssec_validation_enabled, dnssec_trusted_keys",
    )  # --- EDNS ---
    edns_udp_size: int | None = Field(
        default=None,
        description="Advertises the EDNS0 buffer size to the upstream server. The value should be between 512 and 4096 bytes. The recommended value is between 512 and 1220 bytes.",
    )
    use_edns_udp_size: bool | None = Field(
        default=None, description="Use flag for: edns_udp_size"
    )  # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- AAAA filter ---
    filter_aaaa: Literal["YES", "NO", "BREAK_DNSSEC"] | str | None = Field(
        default=None, description="The type of AAAA filtering for this DNS view object."
    )
    filter_aaaa_list: list[ViewFilterAaaaList] | None = Field(
        default=None,
        description="Applies AAAA filtering to a named ACL, or to a list of IPv4 addresses and networks from which queries are received. This field does not allow TSIG keys.",
    )
    use_filter_aaaa: bool | None = Field(
        default=None, description="Use flag for: filter_aaaa , filter_aaaa_list"
    )  # --- fixed RRset order ---
    enable_fixed_rrset_order_fqdns: bool | None = Field(
        default=None, description="Determines if the fixed RRset order FQDN is enabled or not."
    )
    fixed_rrset_order_fqdns: list[ViewFixedRrsetOrderFqdns] | None = Field(
        default=None,
        description="The fixed RRset order FQDN. If this field does not contain an empty value, the appliance will automatically set the enable_fixed_rrset_order_fqdns field to 'true', unless the same request sets the enable field to 'false'.",
    )
    use_fixed_rrset_order_fqdns: bool | None = Field(
        default=None,
        description="Use flag for: fixed_rrset_order_fqdns , enable_fixed_rrset_order_fqdns",
    )  # --- forwarders ---
    forward_only: bool | None = Field(
        default=None,
        description="Determines if this DNS view sends queries to forwarders only or not. When the value is True, queries are sent to forwarders only, and not to other internal or Internet root servers.",
    )
    forwarders: list[str] | None = Field(
        default=None,
        description="The list of forwarders for the DNS view. A forwarder is a name server to which other name servers first send their off-site queries. The forwarder builds up a cache of information, avoiding the need for other name servers to send queries off-site.",
    )
    use_forwarders: bool | None = Field(
        default=None, description="Use flag for: forwarders , forward_only"
    )  # --- last queried ACL ---
    last_queried_acl: list[ViewLastQueriedAcl] | None = Field(
        default=None,
        description="Determines last queried ACL for the specified IPv4 or IPv6 addresses and networks in scavenging settings.",
    )  # --- match clients / destinations ---
    enable_match_recursive_only: bool | None = Field(
        default=None,
        description="Determines if the 'match-recursive-only' option in a DNS view is enabled or not.",
    )
    match_clients: list[ViewMatchClients] | None = Field(
        default=None,
        description="A list of forwarders for the match clients. This list specifies a named ACL, or a list of IPv4/IPv6 addresses, networks, TSIG keys of clients that are allowed or denied access to the DNS view.",
    )
    match_destinations: list[ViewMatchDestinations] | None = Field(
        default=None,
        description="A list of forwarders for the match destinations. This list specifies a name ACL, or a list of IPv4/IPv6 addresses, networks, TSIG keys of clients that are allowed or denied access to the DNS view.",
    )  # --- cache TTL ---
    max_cache_ttl: int | None = Field(
        default=None,
        description="The maximum number of seconds to cache ordinary (positive) answers.",
    )
    max_ncache_ttl: int | None = Field(
        default=None,
        description="The maximum number of seconds to cache negative (NXDOMAIN) answers.",
    )
    max_udp_size: int | None = Field(
        default=None,
        description="The value is used by authoritative DNS servers to never send DNS responses larger than the configured value. The value should be between 512 and 4096 bytes. The recommended value is between 512 and 1220 bytes.",
    )
    use_max_cache_ttl: bool | None = Field(default=None, description="Use flag for: max_cache_ttl")
    use_max_ncache_ttl: bool | None = Field(
        default=None, description="Use flag for: max_ncache_ttl"
    )
    use_max_udp_size: bool | None = Field(
        default=None, description="Use flag for: max_udp_size"
    )  # --- mgm_private ---
    mgm_private: bool | None = Field(
        default=None,
        description="This field controls whether this object is synchronized with the Multi-Grid Master. If this field is set to True, objects are not synchronized.",
    )  # --- NOTIFY ---
    notify_delay: int | None = Field(
        default=None,
        description="The number of seconds of delay the notify messages are sent to secondaries.",
    )  # --- NXDOMAIN redirect ---
    nxdomain_log_query: bool | None = Field(
        default=None,
        description='The flag that indicates whether NXDOMAIN redirection queries are logged. Specify "true" to enable logging, or "false" to disable it. The default value is "false".',
    )
    nxdomain_redirect: bool | None = Field(
        default=None,
        description="Determines if NXDOMAIN redirection in a DNS view is enabled or not.",
    )
    nxdomain_redirect_addresses: list[str] | None = Field(
        default=None,
        description="The array with IPv4 addresses the appliance includes in the response it sends in place of an NXDOMAIN response.",
    )
    nxdomain_redirect_addresses_v6: list[str] | None = Field(
        default=None,
        description="The array with IPv6 addresses the appliance includes in the response it sends in place of an NXDOMAIN response.",
    )
    nxdomain_redirect_ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value of the synthetic DNS responses resulted from NXDOMAIN redirection. The TTL value is a 32-bit unsigned integer that represents the TTL in seconds.",
    )
    nxdomain_rulesets: list[str] | None = Field(
        default=None,
        description="The names of the Ruleset objects assigned at the grid level for NXDOMAIN redirection.",
    )
    use_nxdomain_redirect: bool | None = Field(
        default=None,
        description="Use flag for: nxdomain_redirect , nxdomain_redirect_addresses, nxdomain_redirect_addresses_v6, nxdomain_redirect_ttl, nxdomain_log_query, nxdomain_rulesets",
    )  # --- recursion ---
    recursion: bool | None = Field(
        default=None, description="Determines if recursion is enabled or not."
    )
    use_recursion: bool | None = Field(
        default=None, description="Use flag for: recursion"
    )  # --- response rate limiting ---
    response_rate_limiting: ViewResponseRateLimiting | None = Field(
        default=None, description="Response rate-limiting (RRL) settings."
    )
    use_response_rate_limiting: bool | None = Field(
        default=None, description="Use flag for: response_rate_limiting"
    )  # --- RPZ ---
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
        default=None,
        description="The flag that indicates whether recursive RPZ lookups are enabled.",
    )
    use_rpz_drop_ip_rule: bool | None = Field(
        default=None,
        description="Use flag for: rpz_drop_ip_rule_enabled , rpz_drop_ip_rule_min_prefix_length_ipv4, rpz_drop_ip_rule_min_prefix_length_ipv6",
    )
    use_rpz_qname_wait_recurse: bool | None = Field(
        default=None, description="Use flag for: rpz_qname_wait_recurse"
    )  # --- scavenging ---
    run_scavenging: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the run-scavenging operation."
    )
    scavenging_settings: ViewScavengingSettings | None = Field(
        default=None, description="DNS scavenging settings."
    )
    use_scavenging_settings: bool | None = Field(
        default=None, description="Use flag for: scavenging_settings , last_queried_acl"
    )  # --- sortlist ---
    sortlist: list[ViewSortlist] | None = Field(
        default=None,
        description="A sort list that determines the order of IP addresses in responses sent to DNS queries.",
    )
    use_sortlist: bool | None = Field(default=None, description="Use flag for: sortlist")
