# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneRp - NIOS Response Policy Zone (RPZ).

All 53 properties from ``components.schemas.ZoneRp`` in the v2.14 DNS
swagger are represented here.  The ``fireeye_rule_mapping`` nested object is
typed inline; ``copy_rpz_records`` is a function-type field approximated as
``dict[str, Any]``.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import ExtServer, MemberServer, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "display_domain",
        "dns_soa_email",
        "locked_by",
        "mask_prefix",
        "member_soa_serials",
        "network_view",
        "parent",
        "primary_type",
        "rpz_last_updated_time",
        "rpz_priority",
        "rpz_priority_end",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# ZoneRp-only nested types
# ---------------------------------------------------------------------------


class ZoneRpMemberSoaMnames(_DnsNested):
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
    )  # RO in ZoneAuth equivalent


class ZoneRpMemberSoaSerials(_DnsNested):
    """member_soa_serials list entry (all RO)."""

    grid_primary: str | None = Field(
        default=None, description="The grid primary servers for this zone."
    )  # RO
    ms_server_primary: str | None = Field(
        default=None,
        description='The primary MS server for the zone. Only one of "grid_primary" or "ms_server_primary" will be set when the object is retrieved from the server.',
    )  # RO
    serial: int | None = Field(default=None, description="The SOA serial number.")  # RO


class ZoneRpFireeyeRuleMapping(_DnsNested):
    """fireeye_rule_mapping block.

    ``fireeye_alert_mapping`` is a list of alert-to-RPZ-policy mapping entries;
    typed as ``list[dict[str, Any]]`` as the sub-schema is FireEye-specific and
    rarely configured.
    """

    apt_override: (
        Literal["PASSTHRU", "NXDOMAIN", "NODATA", "SUBSTITUTE", "NOOVERRIDE"] | str | None
    ) = Field(default=None, description="The override setting for APT alerts.")
    fireeye_alert_mapping: list[dict[str, Any]] | None = Field(
        default=None, description="The FireEye alert mapping."
    )
    substituted_domain_name: str | None = Field(
        default=None,
        description='The domain name to be substituted, this is applicable only when apt_override is set to "SUBSTITUTE".',
    )  # ---------------------------------------------------------------------------


# Main ZoneRp model
# ---------------------------------------------------------------------------


class ZoneRp(BaseModel):
    """NIOS Response Policy Zone.

    All 53 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS` and stripped by :class:`ZoneRpResource` on PUT.

    Approximated fields:
    - ``copy_rpz_records``: function-type field; typed as ``dict[str, Any]``.
    - ``lock_unlock_zone``: function-type field; typed as ``dict[str, Any]``.
    - ``fireeye_rule_mapping.fireeye_alert_mapping``: list of alert mappings;
      typed as ``list[dict[str, Any]]`` - see dns/NOTES.md.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    fqdn: str | None = Field(default=None, description="The name of this DNS zone in FQDN format.")
    view: str | None = Field(
        default=None,
        description='The name of the DNS view in which the zone resides. Example "external".',
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
    primary_type: Literal["External", "Grid", "None"] | str | None = Field(
        default=None, description="The type of the primary server."
    )  # RO
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO

    # --- RPZ policy ---
    rpz_policy: (
        Literal["DISABLED", "GIVEN", "NODATA", "NXDOMAIN", "PASSTHRU", "SUBSTITUTE"] | str | None
    ) = Field(default=None, description="The response policy zone override policy.")
    rpz_severity: Literal["CRITICAL", "MAJOR", "WARNING", "INFORMATIONAL"] | str | None = Field(
        default=None, description="The severity of this response policy zone."
    )
    rpz_type: Literal["LOCAL", "FIREEYE", "FEED"] | str | None = Field(
        default=None, description="The type of rpz zone."
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
    rpz_last_updated_time: int | None = Field(
        default=None, description="The timestamp of the last update for zone data."
    )  # RO
    rpz_priority: int | None = Field(
        default=None, description="The priority of this response policy zone."
    )  # RO
    rpz_priority_end: int | None = Field(
        default=None,
        description="This number is for UI to identify the end of qualified zone list.",
    )  # RO
    log_rpz: bool | None = Field(
        default=None,
        description="Determines whether RPZ logging enabled or not at zone level. When this is set to False, the logging is disabled.",
    )
    use_log_rpz: bool | None = Field(default=None, description="Use flag for: log_rpz")
    use_rpz_drop_ip_rule: bool | None = Field(
        default=None,
        description="Use flag for: rpz_drop_ip_rule_enabled , rpz_drop_ip_rule_min_prefix_length_ipv4, rpz_drop_ip_rule_min_prefix_length_ipv6",
    )
    substitute_name: str | None = Field(
        default=None,
        description="The canonical name of redirect target in substitute policy of response policy zone.",
    )  # --- name servers ---
    ns_group: str | None = Field(
        default=None, description="The name server group that serves DNS for this zone."
    )
    prefix: str | None = Field(
        default=None,
        description="The RFC2317 prefix value of this DNS zone. Use this field only when the netmask is greater than 24 bits; that is, for a mask between 25 and 31 bits. Enter a prefix, such as the name of the allocated address block. The prefix can be alphanumeric characters, such as 128/26 , 128-189 , or sub-B.",
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
    grid_secondaries: list[MemberServer] | None = Field(
        default=None,
        description="The list with Grid members that are secondary servers for this zone.",
    )  # --- member SOA ---
    member_soa_mnames: list[ZoneRpMemberSoaMnames] | None = Field(
        default=None, description="The list of per-member SOA MNAME information."
    )
    member_soa_serials: list[ZoneRpMemberSoaSerials] | None = Field(
        default=None, description="The list of per-member SOA serial information."
    )  # RO

    # --- SOA ---
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
    )  # --- record name policy ---
    record_name_policy: str | None = Field(
        default=None, description="The hostname policy for records under this zone."
    )
    use_record_name_policy: bool | None = Field(
        default=None, description="Use flag for: record_name_policy"
    )  # --- FireEye ---
    fireeye_rule_mapping: ZoneRpFireeyeRuleMapping | None = Field(
        default=None
    )  # --- copy RPZ records (function) ---
    copy_rpz_records: dict[str, Any] | None = Field(default=None)  # function-type field

    # --- lock ---
    lock_unlock_zone: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the lock/unlock-zone operation."
    )  # function-type field
    locked: bool | None = Field(
        default=None,
        description="If you enable this flag, other administrators cannot make conflicting changes. This is for administration purposes only. The zone will continue to serve DNS data even when it is locked.",
    )
    locked_by: str | None = Field(
        default=None,
        description="The name of a superuser or the administrator who locked this zone.",
    )  # RO

    # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
