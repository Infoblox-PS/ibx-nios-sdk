# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneStub - NIOS stub DNS zone.

All 38 properties from ``components.schemas.ZoneStub`` in the v2.14 DNS
swagger are represented here.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import MemberServer, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "display_domain",
        "dns_fqdn",
        "locked_by",
        "mask_prefix",
        "mgm_private_overridable",
        "ms_managed",
        "ms_read_only",
        "ms_sync_master_name",
        "parent",
        "soa_email",
        "soa_expire",
        "soa_mname",
        "soa_negative_ttl",
        "soa_refresh",
        "soa_retry",
        "soa_serial_number",
        "using_srg_associations",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# ZoneStub-only nested types
# ---------------------------------------------------------------------------


class ZoneStubStubFrom(_DnsNested):
    """stub_from list entry - authoritative server for the stub zone.

    Same 8-field shape as ExtServer.
    """

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )
    name: str | None = Field(
        default=None, description="A resolvable domain name for the external DNS server."
    )
    shared_with_ms_parent_delegation: bool | None = Field(
        default=None,
        description="This flag represents whether the name server is shared with the parent Microsoft primary zone's delegation server.",
    )
    stealth: bool | None = Field(
        default=None,
        description="Set this flag to hide the NS record for the primary name server from DNS queries.",
    )
    tsig_key: str | None = Field(default=None, description="A generated TSIG key.")
    tsig_key_alg: Literal["HMAC-MD5", "HMAC-SHA256"] | str | None = Field(
        default=None, description="The TSIG key algorithm."
    )
    tsig_key_name: str | None = Field(default=None, description="The TSIG key name.")
    use_tsig_key_name: bool | None = Field(default=None, description="Use flag for: tsig_key_name")


class ZoneStubStubMsservers(_DnsNested):
    """stub_msservers list entry - MS server for stub zone."""

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
    )  # ---------------------------------------------------------------------------


# Main ZoneStub model
# ---------------------------------------------------------------------------


class ZoneStub(BaseModel):
    """NIOS stub DNS zone.

    All 38 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS` and stripped by :class:`ZoneStubResource` on PUT.

    Note: ``soa_email``, ``soa_expire``, ``soa_mname``, ``soa_negative_ttl``,
    ``soa_refresh``, ``soa_retry``, and ``soa_serial_number`` are all readOnly
    in the swagger - stubs receive SOA data from the primary server.
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
    mask_prefix: str | None = Field(
        default=None, description="IPv4 Netmask or IPv6 prefix for this zone."
    )  # RO
    parent: str | None = Field(
        default=None,
        description='The parent zone of this zone. Note that when searching for reverse zones, the "in-addr.arpa" notation should be used.',
    )  # RO
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO

    # --- stub config ---
    stub_from: list[ZoneStubStubFrom] | None = Field(
        default=None, description="The primary servers (masters) of this stub zone."
    )
    stub_members: list[MemberServer] | None = Field(
        default=None,
        description="The Grid member servers of this stub zone. Note that the lead/stealth/grid_replicate/ preferred_primaries/override_preferred_primaries fields of the struct will be ignored when set in this field.",
    )
    stub_msservers: list[ZoneStubStubMsservers] | None = Field(
        default=None,
        description="The Microsoft DNS servers of this stub zone. Note that the stealth field of the struct will be ignored when set in this field.",
    )
    disable_forwarding: bool | None = Field(
        default=None,
        description="Determines if the name servers that host the zone should not forward queries that end with the domain name of the zone to any configured forwarders.",
    )
    external_ns_group: str | None = Field(
        default=None, description="A forward stub server name server group."
    )
    ns_group: str | None = Field(default=None, description="A stub member name server group.")
    prefix: str | None = Field(
        default=None,
        description="The RFC2317 prefix value of this DNS zone. Use this field only when the netmask is greater than 24 bits; that is, for a mask between 25 and 31 bits. Enter a prefix, such as the name of the allocated address block. The prefix can be alphanumeric characters, such as 128/26 , 128-189 , or sub-B.",
    )  # --- lock ---
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
    ms_read_only: bool | None = Field(
        default=None,
        description="Determines if a Grid member manages the zone served by a Microsoft DNS server in read-only mode. This flag is true when a Grid member manages the zone in read-only mode, false otherwise. When the zone has the ms_read_only flag set to True, no changes can be made to this zone.",
    )  # RO
    ms_sync_master_name: str | None = Field(
        default=None, description="The name of MS synchronization master for this zone."
    )  # RO

    # --- SOA (all RO - populated from primary) ---
    soa_email: str | None = Field(
        default=None,
        description="The SOA email for the zone. This value can be in unicode format.",
    )  # RO
    soa_expire: int | None = Field(
        default=None,
        description="This setting defines the amount of time, in seconds, after which the secondary server stops giving out answers about the zone because the zone data is too old to be useful.",
    )  # RO
    soa_mname: str | None = Field(
        default=None,
        description="The SOA mname value for this zone. The Infoblox appliance allows you to change the name of the primary server on the SOA record that is automatically created when you initially configure a zone. Use this method to change the name of the primary server on the SOA record. For example, you may want to hide the primary server for a zone. If your device is named dns1.zone.tld, and for security reasons, you want to show a secondary server called dns2.zone.tld as the primary server. To do so, you would go to dns1.zone.tld zone (being the true primary) and change the primary server on the SOA to dns2.zone.tld to hide the true identity of the real primary server. This value can be in unicode format.",
    )  # RO
    soa_negative_ttl: int | None = Field(
        default=None,
        description='The negative Time to Live (TTL) value of the SOA of the zone indicates how long a secondary server can cache data for "Does Not Respond" responses.',
    )  # RO
    soa_refresh: int | None = Field(
        default=None,
        description="This indicates the interval at which a secondary server sends a message to the primary server for a zone to check that its data is current, and retrieve fresh data if it is not.",
    )  # RO
    soa_retry: int | None = Field(
        default=None,
        description="This indicates how long a secondary server must wait before attempting to recontact the primary server after a connection failure between the two servers occurs.",
    )  # RO
    soa_serial_number: int | None = Field(
        default=None,
        description="The serial number in the SOA record incrementally changes every time the record is modified. The Infoblox appliance allows you to change the serial number (in the SOA record) for the primary server so it is higher than the secondary server, thereby ensuring zone transfers come from the primary server.",
    )  # RO

    # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- misc ---
    using_srg_associations: bool | None = Field(
        default=None,
        description="This is true if the zone is associated with a shared record group.",
    )  # RO
