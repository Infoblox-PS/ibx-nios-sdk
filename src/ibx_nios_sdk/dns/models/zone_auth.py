# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneAuth - NIOS authoritative DNS zone.

All 129 properties from ``components.schemas.ZoneAuth`` in the v2.14 DNS
swagger are represented here.  Deeply nested ZoneAuth-only schemas that are
complex/rarely written (dnssec_key_params sub-fields, scavenging_schedule,
AWS zone info, function-typed fields) are typed as ``dict[str, Any]``; see
``dns/NOTES.md`` for the full approximated-field list.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import CloudInfo, ExtServer, MemberServer, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "aws_rte53_zone_info",
        "cloud_info",
        "display_domain",
        "dns_fqdn",
        "dns_soa_email",
        "dnssec_ksk_rollover_date",
        "dnssec_zsk_rollover_date",
        "effective_record_name_policy",
        "grid_primary_shared_with_ms_parent_delegation",
        "is_dnssec_enabled",
        "is_dnssec_signed",
        "is_multimaster",
        "last_queried",
        "locked_by",
        "mask_prefix",
        "member_soa_serials",
        "mgm_private_overridable",
        "ms_managed",
        "ms_read_only",
        "ms_sync_master_name",
        "network_associations",
        "network_view",
        "parent",
        "primary_type",
        "records_monitored",
        "rr_not_queried_enabled_time",
        "using_srg_associations",
        "uuid",
        "zone_not_queried_enabled_time",
    }
)


# ---------------------------------------------------------------------------
# ZoneAuth-only nested types
# ---------------------------------------------------------------------------


class ZoneAuthAclEntry(_DnsNested):
    """Generic ACL entry with address, permission, optional TSIG.

    Shared shape for: allow_query, allow_transfer, allow_update,
    update_forwarding, last_queried_acl.
    """

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
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


class ZoneAuthAllowActiveDir(_DnsNested):
    """allow_active_dir list entry (2 fields)."""

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )


class ZoneAuthMsAllowTransfer(_DnsNested):
    """ms_allow_transfer list entry (2 fields)."""

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )


class ZoneAuthMsDcNsRecordCreation(_DnsNested):
    """ms_dc_ns_record_creation list entry."""

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )
    comment: str | None = Field(
        default=None, description="Comment for the zone; maximum 256 characters."
    )


class ZoneAuthMsPrimaries(_DnsNested):
    """ms_primaries list entry - MS primary server."""

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )
    is_master: bool | None = Field(
        default=None, description="This flag indicates if this server is a synchronization master."
    )
    ns_ip: str | None = Field(
        default=None,
        description="This address is used when generating the NS record in the zone, which can be different in case of multihomed hosts.",
    )
    ns_name: str | None = Field(
        default=None,
        description="This name is used when generating the NS record in the zone, which can be different in case of multihomed hosts.",
    )
    stealth: bool | None = Field(
        default=None,
        description="Set this flag to hide the NS record for the primary name server from DNS queries.",
    )
    shared_with_ms_parent_delegation: bool | None = Field(
        default=None,
        description="This flag represents whether the name server is shared with the parent Microsoft primary zone's delegation server.",
    )  # RO per swagger


class ZoneAuthMsSecondaries(_DnsNested):
    """ms_secondaries list entry - MS secondary server."""

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )
    is_master: bool | None = Field(
        default=None, description="This flag indicates if this server is a synchronization master."
    )
    ns_ip: str | None = Field(
        default=None,
        description="This address is used when generating the NS record in the zone, which can be different in case of multihomed hosts.",
    )
    ns_name: str | None = Field(
        default=None,
        description="This name is used when generating the NS record in the zone, which can be different in case of multihomed hosts.",
    )
    stealth: bool | None = Field(
        default=None,
        description="Set this flag to hide the NS record for the primary name server from DNS queries.",
    )
    shared_with_ms_parent_delegation: bool | None = Field(
        default=None,
        description="This flag represents whether the name server is shared with the parent Microsoft primary zone's delegation server.",
    )  # RO per swagger


class ZoneAuthMemberSoaMnames(_DnsNested):
    """member_soa_mnames list entry."""

    grid_primary: str | None = Field(
        default=None, description="The grid primary servers for this zone."
    )
    ms_server_primary: str | None = Field(
        default=None,
        description='The primary MS server for the zone. Only one of "grid_primary" or "ms_server_primary" will be set when the object is retrieved from the server.',
    )
    mname: str | None = Field(
        default=None, description="Master's SOA MNAME. This value can be in unicode format."
    )
    dns_mname: str | None = Field(
        default=None, description="Master's SOA MNAME in punycode format."
    )  # RO


class ZoneAuthMemberSoaSerials(_DnsNested):
    """member_soa_serials list entry (all RO)."""

    grid_primary: str | None = Field(
        default=None, description="The grid primary servers for this zone."
    )  # RO
    ms_server_primary: str | None = Field(
        default=None,
        description='The primary MS server for the zone. Only one of "grid_primary" or "ms_server_primary" will be set when the object is retrieved from the server.',
    )  # RO
    serial: int | None = Field(default=None, description="The SOA serial number.")  # RO


class ZoneAuthDnssecKeyParams(_DnsNested):
    """DNSSEC key parameters block.

    ``ksk_algorithms`` and ``zsk_algorithms`` are arrays of nested objects
    (``ZoneauthdnseckeyparamsKskAlgorithms``); typed as ``list[dict[str, Any]]``
    (see dns/NOTES.md).
    """

    enable_ksk_auto_rollover: bool | None = Field(
        default=None,
        description="If set to True, automatic rollovers for the signing key is enabled.",
    )
    ksk_algorithm: Literal["10", "5", "7", "8", "13", "14"] | str | None = Field(
        default=None, description="Key Signing Key algorithm. Deprecated."
    )
    ksk_algorithms: list[dict[str, Any]] | None = Field(
        default=None, description="A list of Key Signing Key Algorithms."
    )
    ksk_rollover: int | None = Field(
        default=None, description="Key Signing Key rollover interval, in seconds."
    )
    ksk_size: int | None = Field(
        default=None, description="Key Signing Key size, in bits. Deprecated."
    )
    next_secure_type: Literal["NSEC", "NSEC3"] | str | None = Field(
        default=None, description="NSEC (next secure) types."
    )
    ksk_rollover_notification_config: (
        Literal["NONE", "ALL", "REQUIRE_MANUAL_INTERVENTION"] | str | None
    ) = Field(
        default=None, description="This field controls events for which users will be notified."
    )
    ksk_snmp_notification_enabled: bool | None = Field(
        default=None, description="Enable SNMP notifications for KSK related events."
    )
    ksk_email_notification_enabled: bool | None = Field(
        default=None, description="Enable email notifications for KSK related events."
    )
    nsec3_salt_min_length: int | None = Field(
        default=None,
        description="The minimum length for NSEC3 salts. RFC 9276 recommends empty salt (0 octets) for optimal resolver compatibility and reduced computational overhead.",
    )
    nsec3_salt_max_length: int | None = Field(
        default=None,
        description="The maximum length for NSEC3 salts. RFC 9276 recommends empty salt (0 octets) for optimal resolver compatibility and reduced computational overhead.",
    )
    nsec3_iterations: int | None = Field(
        default=None,
        description="The number of iterations used for hashing NSEC3. RFC 9276 Section 3.1 mandates that this value MUST be set to zero (0) to ensure DNSSEC resolver compatibility and alleviate computational burdens on validating resolvers.",
    )
    signature_expiration: int | None = Field(
        default=None, description="Signature expiration time, in seconds."
    )
    zsk_algorithm: Literal["10", "5", "7", "8", "13", "14"] | str | None = Field(
        default=None, description="Zone Signing Key algorithm. Deprecated."
    )
    zsk_algorithms: list[dict[str, Any]] | None = Field(
        default=None, description="A list of Zone Signing Key Algorithms."
    )
    zsk_rollover: int | None = Field(
        default=None, description="Zone Signing Key rollover interval, in seconds."
    )
    zsk_rollover_mechanism: Literal["DOUBLE_SIGN", "PRE_PUBLISH"] | str | None = Field(
        default=None, description="Zone Signing Key rollover mechanism."
    )
    zsk_size: int | None = Field(
        default=None, description="Zone Signing Key size, in bits. Deprecated."
    )


class ZoneAuthDnssecKeys(_DnsNested):
    """dnssec_keys list entry (all fields RO)."""

    tag: int | None = Field(default=None, description="The tag of the key for the zone.")
    status: Literal["ACTIVE", "PUBLISHED", "ROLLED", "IMPORTED"] | str | None = Field(
        default=None, description="The status of the key for the zone."
    )  # RO
    next_event_date: int | None = Field(
        default=None,
        description="The next event date for the key, the rollover date for an active key or the removal date for an already rolled one.",
    )  # RO
    type_: Literal["KSK", "ZSK"] | str | None = Field(
        default=None, alias="type", description="Object type discriminator."
    )  # RO
    algorithm: Literal["10", "5", "7", "8", "13", "14"] | str | None = Field(
        default=None,
        description="The public-key encryption algorithm. Values 1, 3 and 6 are deprecated from NIOS 9.0.",
    )  # RO
    public_key: str | None = Field(
        default=None, description="The Base-64 encoding of the public key."
    )  # RO


class ZoneAuthScavengingSettings(_DnsNested):
    """Scavenging configuration block.

    ``scavenging_schedule``, ``expression_list``, ``ea_expression_list`` are
    typed as ``dict``/``list[dict]`` - see dns/NOTES.md.
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
    )  # ---------------------------------------------------------------------------


# Main ZoneAuth model
# ---------------------------------------------------------------------------


class ZoneAuth(BaseModel):
    """NIOS authoritative DNS zone.

    All 129 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS` and stripped by :class:`ZoneAuthResource` on PUT.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    fqdn: str | None = Field(
        default=None,
        description='The name of this DNS zone. For a reverse zone, this is in "address/cidr" format. For other zones, this is in FQDN format. This value can be in unicode format. Note that for a reverse zone, the corresponding zone_format value should be set.',
    )
    view: str | None = Field(
        default=None,
        description='The name of the DNS view in which the zone resides. Example "external".',
    )
    zone_format: Literal["FORWARD", "IPV4", "IPV6"] | str | None = Field(
        default=None, description="Determines the format of this zone."
    )
    comment: str | None = Field(
        default=None, description="Comment for the zone; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a zone is disabled or not. When this is set to False, the zone is enabled.",
    )  # --- read-only identity ---
    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )  # RO
    display_domain: str | None = Field(
        default=None, description="The displayed name of the DNS zone."
    )  # RO
    dns_fqdn: str | None = Field(
        default=None,
        description='The name of this DNS zone in punycode format. For a reverse zone, this is in "address/cidr" format. For other zones, this is in FQDN format in punycode format.',
    )  # RO
    dns_soa_email: str | None = Field(
        default=None, description="The SOA email for the zone in punycode format."
    )  # RO
    mask_prefix: str | None = Field(
        default=None, description="IPv4 Netmask or IPv6 prefix for this zone."
    )  # RO
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this zone resides."
    )  # RO
    parent: str | None = Field(
        default=None,
        description='The parent zone of this zone. Note that when searching for reverse zones, the "in-addr.arpa" notation should be used.',
    )  # RO
    prefix: str | None = Field(
        default=None,
        description="The RFC2317 prefix value of this DNS zone. Use this field only when the netmask is greater than 24 bits; that is, for a mask between 25 and 31 bits. Enter a prefix, such as the name of the allocated address block. The prefix can be alphanumeric characters, such as 128/26 , 128-189 , or sub-B.",
    )
    primary_type: Literal["External", "Grid", "Microsoft", "None"] | str | None = Field(
        default=None, description="The type of the primary server."
    )  # RO
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO

    # --- allow lists / ACLs ---
    allow_active_dir: list[ZoneAuthAllowActiveDir] | None = Field(
        default=None,
        description="This field allows the zone to receive GSS-TSIG authenticated DDNS updates from DHCP clients and servers in an AD domain. Note that addresses specified in this field ignore the permission set in the struct which will be set to 'ALLOW'.",
    )
    allow_fixed_rrset_order: bool | None = Field(
        default=None,
        description="The flag that allows to enable or disable fixed RRset ordering for authoritative forward-mapping zones.",
    )
    allow_gss_tsig_for_underscore_zone: bool | None = Field(
        default=None,
        description="The flag that allows DHCP clients to perform GSS-TSIG signed updates for underscore zones.",
    )
    allow_gss_tsig_zone_updates: bool | None = Field(
        default=None,
        description="The flag that enables or disables the zone for GSS-TSIG updates.",
    )
    allow_query: list[ZoneAuthAclEntry] | None = Field(
        default=None,
        description="Determines whether DNS queries are allowed from a named ACL, or from a list of IPv4/IPv6 addresses, networks, and TSIG keys for the hosts.",
    )
    allow_transfer: list[ZoneAuthAclEntry] | None = Field(
        default=None,
        description="Determines whether zone transfers are allowed from a named ACL, or from a list of IPv4/IPv6 addresses, networks, and TSIG keys for the hosts.",
    )
    allow_update: list[ZoneAuthAclEntry] | None = Field(
        default=None,
        description="Determines whether dynamic DNS updates are allowed from a named ACL, or from a list of IPv4/IPv6 addresses, networks, and TSIG keys for the hosts.",
    )
    allow_update_forwarding: bool | None = Field(
        default=None,
        description="The list with IP addresses, networks or TSIG keys for clients, from which forwarded dynamic updates are allowed.",
    )
    update_forwarding: list[ZoneAuthAclEntry] | None = Field(
        default=None,
        description="Use this field to allow or deny dynamic DNS updates that are forwarded from specific IPv4/IPv6 addresses, networks, or a named ACL. You can also provide TSIG keys for clients that are allowed or denied to perform zone updates. This setting overrides the member-level setting.",
    )
    last_queried_acl: list[ZoneAuthAclEntry] | None = Field(
        default=None,
        description="Determines last queried ACL for the specified IPv4 or IPv6 addresses and networks in scavenging settings.",
    )  # --- AWS Route53 ---
    aws_rte53_zone_info: dict[str, Any] | None = Field(
        default=None
    )  # All RO sub-fields; see NOTES.md

    # --- cloud ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # RO in practice

    # --- copy zone records (function) ---
    copyzonerecords: dict[str, Any] | None = Field(
        default=None
    )  # function-type field; see NOTES.md

    # --- host abstraction ---
    create_ptr_for_bulk_hosts: bool | None = Field(
        default=None,
        description="Determines if PTR records are created for hosts automatically, if necessary, when the zone data is imported. This field is meaningful only when import_from is set.",
    )
    create_ptr_for_hosts: bool | None = Field(
        default=None,
        description="Determines if PTR records are created for hosts automatically, if necessary, when the zone data is imported. This field is meaningful only when import_from is set.",
    )
    create_underscore_zones: bool | None = Field(
        default=None,
        description="Determines whether automatic creation of subzones is enabled or not.",
    )
    do_host_abstraction: bool | None = Field(
        default=None,
        description="Determines if hosts and bulk hosts are automatically created when the zone data is imported. This field is meaningful only when import_from is set.",
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
    )  # --- check names policy ---
    effective_check_names_policy: Literal["FAIL", "WARN"] | str | None = Field(
        default=None,
        description='The value of the check names policy, which indicates the action the appliance takes when it encounters host names that do not comply with the Strict Hostname Checking policy. This value applies only if the host name restriction policy is set to "Strict Hostname Checking".',
    )
    use_check_names_policy: bool | None = Field(
        default=None,
        description='Apply policy to dynamic updates and inbound zone transfers (This value applies only if the host name restriction policy is set to "Strict Hostname Checking".)',
    )
    effective_record_name_policy: str | None = Field(
        default=None, description="The selected hostname policy for records under this zone."
    )  # RO
    record_name_policy: str | None = Field(
        default=None, description="The hostname policy for records under this zone."
    )
    use_record_name_policy: bool | None = Field(
        default=None, description="Use flag for: record_name_policy"
    )  # --- DNS integrity ---
    dns_integrity_enable: bool | None = Field(
        default=None,
        description="If this is set to True, DNS integrity check is enabled for this zone.",
    )
    dns_integrity_frequency: int | None = Field(
        default=None,
        description="The frequency, in seconds, of DNS integrity checks for this zone.",
    )
    dns_integrity_member: str | None = Field(
        default=None,
        description="The Grid member that performs DNS integrity checks for this zone.",
    )
    dns_integrity_verbose_logging: bool | None = Field(
        default=None,
        description="If this is set to True, more information is logged for DNS integrity checks for this zone.",
    )  # --- DNSSEC ---
    dnssec_export: dict[str, Any] | None = Field(default=None)  # function-type; see NOTES.md
    dnssec_get_zone_keys: dict[str, Any] | None = Field(
        default=None
    )  # function-type; see NOTES.md
    dnssec_key_params: ZoneAuthDnssecKeyParams | None = Field(
        default=None, description="DNSSEC key generation parameters."
    )
    dnssec_keys: list[ZoneAuthDnssecKeys] | None = Field(
        default=None, description="A list of DNSSEC keys for the zone."
    )
    dnssec_ksk_rollover_date: int | None = Field(
        default=None, description="The rollover date for the Key Signing Key."
    )  # RO
    dnssec_operation: dict[str, Any] | None = Field(default=None)  # function-type; see NOTES.md
    dnssec_set_zone_keys: dict[str, Any] | None = Field(
        default=None
    )  # function-type; see NOTES.md
    dnssec_zsk_rollover_date: int | None = Field(
        default=None, description="The rollover date for the Zone Signing Key."
    )  # RO
    dnssecgetkskrollover: dict[str, Any] | None = Field(
        default=None
    )  # function-type; see NOTES.md
    is_dnssec_enabled: bool | None = Field(
        default=None, description="This flag is set to True if DNSSEC is enabled for the zone."
    )  # RO
    is_dnssec_signed: bool | None = Field(
        default=None, description="Determines if the zone is DNSSEC signed."
    )  # RO
    use_dnssec_key_params: bool | None = Field(
        default=None, description="Use flag for: dnssec_key_params"
    )  # --- execute DNS parent check (function) ---
    execute_dns_parent_check: dict[str, Any] | None = Field(
        default=None
    )  # function-type; see NOTES.md

    # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- external primaries / secondaries ---
    external_primaries: list[ExtServer] | None = Field(
        default=None, description="The list of external primary servers."
    )
    external_secondaries: list[ExtServer] | None = Field(
        default=None, description="The list of external secondary servers."
    )
    use_external_primary: bool | None = Field(
        default=None,
        description="This flag controls whether the zone is using an external primary.",
    )  # --- grid primary / secondaries ---
    grid_primary: list[MemberServer] | None = Field(
        default=None, description="The grid primary servers for this zone."
    )
    grid_primary_shared_with_ms_parent_delegation: bool | None = Field(
        default=None, description="Determines if the server is duplicated with parent delegation."
    )  # RO
    grid_secondaries: list[MemberServer] | None = Field(
        default=None,
        description="The list with Grid members that are secondary servers for this zone.",
    )
    is_multimaster: bool | None = Field(
        default=None, description="Determines if multi-master DNS is enabled for the zone."
    )  # RO

    # --- import ---
    import_from: str | None = Field(
        default=None,
        description="The IP address of the Infoblox appliance from which zone data is imported. Setting this address to '255.255.255.255' and do_host_abstraction to 'true' will create Host records from A records in this zone without importing zone data.",
    )
    use_import_from: bool | None = Field(
        default=None, description="Use flag for: import_from"
    )  # --- last queried ---
    last_queried: int | None = Field(
        default=None, description="The time the zone was last queried on."
    )  # RO
    rr_not_queried_enabled_time: int | None = Field(
        default=None,
        description="The time data collection for Not Queried Resource Record was enabled for this zone.",
    )  # RO
    zone_not_queried_enabled_time: int | None = Field(
        default=None,
        description='The time when "DNS Zones Last Queried" was turned on for this zone.',
    )  # RO

    # --- lock ---
    lock_unlock_zone: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the lock/unlock-zone operation."
    )  # function-type; see NOTES.md
    locked: bool | None = Field(
        default=None,
        description="If you enable this flag, other administrators cannot make conflicting changes. This is for administration purposes only. The zone will continue to serve DNS data even when it is locked.",
    )
    locked_by: str | None = Field(
        default=None,
        description="The name of a superuser or the administrator who locked this zone.",
    )  # RO

    # --- member SOA ---
    member_soa_mnames: list[ZoneAuthMemberSoaMnames] | None = Field(
        default=None, description="The list of per-member SOA MNAME information."
    )
    member_soa_serials: list[ZoneAuthMemberSoaSerials] | None = Field(
        default=None, description="The list of per-member SOA serial information."
    )  # RO

    # --- mgm ---
    mgm_private: bool | None = Field(
        default=None,
        description="This field controls whether this object is synchronized with the Multi-Grid Master. If this field is set to True, objects are not synchronized.",
    )
    mgm_private_overridable: bool | None = Field(
        default=None,
        description="This field is assumed to be True unless filled by any conforming objects, such as Network, IPv6 Network, Network Container, IPv6 Network Container, and Network View. This value is set to False if mgm_private is set to True in the parent object.",
    )  # RO

    # --- MS integration ---
    ms_ad_integrated: bool | None = Field(
        default=None,
        description='The flag that determines whether Active Directory is integrated or not. This field is valid only when ms_managed is "STUB", "AUTH_PRIMARY", or "AUTH_BOTH".',
    )
    ms_allow_transfer: list[ZoneAuthMsAllowTransfer] | None = Field(
        default=None,
        description="The list of DNS clients that are allowed to perform zone transfers from a Microsoft DNS server. This setting applies only to zones with Microsoft DNS servers that are either primary or secondary servers. This setting does not inherit any value from the Grid or from any member that defines an allow_transfer value. This setting does not apply to any grid member. Use the allow_transfer field to control which DNS clients are allowed to perform zone transfers on Grid members.",
    )
    ms_allow_transfer_mode: Literal["ADDRESS_AC", "ANY", "ANY_NS", "NONE"] | str | None = Field(
        default=None,
        description='Determines which DNS clients are allowed to perform zone transfers from a Microsoft DNS server. Valid values are: "ADDRESS_AC", to use ms_allow_transfer field for specifying IP addresses, networks and Transaction Signature (TSIG) keys for clients that are allowed to do zone transfers. "ANY", to allow any client. "ANY_NS", to allow only the nameservers listed in this zone. "NONE", to deny all zone transfer requests.',
    )
    ms_dc_ns_record_creation: list[ZoneAuthMsDcNsRecordCreation] | None = Field(
        default=None,
        description="The list of domain controllers that are allowed to create NS records for authoritative zones.",
    )
    ms_ddns_mode: Literal["ANY", "NONE", "SECURE"] | str | None = Field(
        default=None,
        description='Determines whether an Active Directory-integrated zone with a Microsoft DNS server as primary allows dynamic updates. Valid values are: "SECURE" if the zone allows secure updates only. "NONE" if the zone forbids dynamic updates. "ANY" if the zone accepts both secure and nonsecure updates. This field is valid only if ms_managed is either "AUTH_PRIMARY" or "AUTH_BOTH". If the flag ms_ad_integrated is false, the value "SECURE" is not allowed.',
    )
    ms_managed: (
        Literal["AUTH_BOTH", "AUTH_PRIMARY", "AUTH_SECONDARY", "NONE", "STUB"] | str | None
    ) = Field(
        default=None,
        description='The flag that indicates whether the zone is assigned to a Microsoft DNS server. This flag returns the authoritative name server type of the Microsoft DNS server. Valid values are: "NONE" if the zone is not assigned to any Microsoft DNS server. "STUB" if the zone is assigned to a Microsoft DNS server as a stub zone. "AUTH_PRIMARY" if only the primary server of the zone is a Microsoft DNS server. "AUTH_SECONDARY" if only the secondary server of the zone is a Microsoft DNS server. "AUTH_BOTH" if both the primary and secondary servers of the zone are Microsoft DNS servers.',
    )  # RO
    ms_primaries: list[ZoneAuthMsPrimaries] | None = Field(
        default=None,
        description="The list with the Microsoft DNS servers that are primary servers for the zone. Although a zone typically has just one primary name server, you can specify up to ten independent servers for a single zone.",
    )
    ms_read_only: bool | None = Field(
        default=None,
        description="Determines if a Grid member manages the zone served by a Microsoft DNS server in read-only mode. This flag is true when a Grid member manages the zone in read-only mode, false otherwise. When the zone has the ms_read_only flag set to True, no changes can be made to this zone.",
    )  # RO
    ms_secondaries: list[ZoneAuthMsSecondaries] | None = Field(
        default=None,
        description="The list with the Microsoft DNS servers that are secondary servers for the zone.",
    )
    ms_sync_disabled: bool | None = Field(
        default=None,
        description="This flag controls whether this zone is synchronized with Microsoft DNS servers.",
    )
    ms_sync_master_name: str | None = Field(
        default=None, description="The name of MS synchronization master for this zone."
    )  # RO

    # --- network associations ---
    network_associations: list[Any] | None = Field(
        default=None,
        description="The list with the associated network/network container information.",
    )  # RO; items have no $ref in swagger

    # --- notify ---
    notify_delay: int | None = Field(
        default=None,
        description="The number of seconds in delay with which notify messages are sent to secondaries.",
    )
    copy_xfer_to_notify: bool | None = Field(
        default=None,
        description="If this flag is set to True then copy allowed IPs from Allow Transfer to Also Notify.",
    )
    use_copy_xfer_to_notify: bool | None = Field(
        default=None, description="Use flag for: copy_xfer_to_notify"
    )
    use_notify_delay: bool | None = Field(
        default=None, description="Use flag for: notify_delay"
    )  # --- NS group / forwarding ---
    ns_group: str | None = Field(
        default=None, description="The name server group that serves DNS for this zone."
    )
    disable_forwarding: bool | None = Field(
        default=None,
        description="Determines whether the name servers that host the zone should forward queries (ended with the domain name of the zone) to any configured forwarders.",
    )  # --- records ---
    records_monitored: bool | None = Field(
        default=None, description="Determines if this zone is also monitoring resource records."
    )  # RO
    remove_subzones: bool | None = Field(
        default=None,
        description="Remove subzones delete option. Determines whether all child objects should be removed alongside with the parent zone or child objects should be assigned to another parental zone. By default child objects are deleted with the parent zone.",
    )
    srgs: list[Any] | None = Field(
        default=None,
        description="The associated shared record groups of a DNS zone. If a shared record group is associated with a zone, then all shared records in a shared record group will be shared in the zone.",
    )
    using_srg_associations: bool | None = Field(
        default=None,
        description="This is true if the zone is associated with a shared record group.",
    )  # RO

    # --- restart ---
    restart_if_needed: bool | None = Field(
        default=None, description="Restarts the member service."
    )  # --- run scavenging (function) ---
    run_scavenging: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the run-scavenging operation."
    )  # function-type; see NOTES.md

    # --- scavenging ---
    scavenging_settings: ZoneAuthScavengingSettings | None = Field(
        default=None, description="DNS scavenging settings."
    )
    use_scavenging_settings: bool | None = Field(
        default=None, description="Use flag for: scavenging_settings , last_queried_acl"
    )  # --- SOA ---
    set_soa_serial_number: bool | None = Field(
        default=None,
        description='The serial number in the SOA record incrementally changes every time the record is modified. The Infoblox appliance allows you to change the serial number (in the SOA record) for the primary server so it is higher than the secondary server, thereby ensuring zone transfers come from the primary server (as they should). To change the serial number you need to set a new value at "soa_serial_number" and pass "set_soa_serial_number" as True.',
    )
    soa_default_ttl: int | None = Field(
        default=None,
        description="The Time to Live (TTL) value of the SOA record of this zone. This value is the number of seconds that data is cached.",
    )
    soa_email: str | None = Field(
        default=None,
        description="The SOA email value for this zone. This value can be in unicode format.",
    )
    soa_expire: int | None = Field(
        default=None,
        description="This setting defines the amount of time, in seconds, after which the secondary server stops giving out answers about the zone because the zone data is too old to be useful. The default is one week.",
    )
    soa_negative_ttl: int | None = Field(
        default=None,
        description='The negative Time to Live (TTL) value of the SOA of the zone indicates how long a secondary server can cache data for "Does Not Respond" responses.',
    )
    soa_refresh: int | None = Field(
        default=None,
        description="This indicates the interval at which a secondary server sends a message to the primary server for a zone to check that its data is current, and retrieve fresh data if it is not.",
    )
    soa_retry: int | None = Field(
        default=None,
        description="This indicates how long a secondary server must wait before attempting to recontact the primary server after a connection failure between the two servers occurs.",
    )
    soa_serial_number: int | None = Field(
        default=None,
        description='The serial number in the SOA record incrementally changes every time the record is modified. The Infoblox appliance allows you to change the serial number (in the SOA record) for the primary server so it is higher than the secondary server, thereby ensuring zone transfers come from the primary server (as they should). To change the serial number you need to set a new value at "soa_serial_number" and pass "set_soa_serial_number" as True.',
    )
    use_grid_zone_timer: bool | None = Field(
        default=None,
        description="Use flag for: soa_default_ttl , soa_expire, soa_negative_ttl, soa_refresh, soa_retry",
    )
    use_soa_email: bool | None = Field(
        default=None, description="Use flag for: soa_email"
    )  # --- allow query / transfer / update use flags ---
    use_allow_active_dir: bool | None = Field(
        default=None, description="Use flag for: allow_active_dir"
    )
    use_allow_query: bool | None = Field(default=None, description="Use flag for: allow_query")
    use_allow_transfer: bool | None = Field(
        default=None, description="Use flag for: allow_transfer"
    )
    use_allow_update: bool | None = Field(default=None, description="Use flag for: allow_update")
    use_allow_update_forwarding: bool | None = Field(
        default=None, description="Use flag for: allow_update_forwarding"
    )
