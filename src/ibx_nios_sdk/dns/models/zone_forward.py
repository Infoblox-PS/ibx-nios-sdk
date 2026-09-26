# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneForward - NIOS forward DNS zone.

All 31 properties from ``components.schemas.ZoneForward`` in the v2.14 DNS
swagger are represented here.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import ExtServer, _DnsNested

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
        "using_srg_associations",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# ZoneForward-only nested types
# ---------------------------------------------------------------------------


class ZoneForwardForwardTo(_DnsNested):
    """forward_to list entry - external forward server.

    Same 8-field shape as ExtServer; aliased here for clarity.
    ``shared_with_ms_parent_delegation`` is not in the swagger readOnly list
    for this nested type but is effectively informational.
    """

    address: str | None = Field(
        default=None, description="The IP address of the server that is serving this zone."
    )
    name: str | None = Field(
        default=None, description="The name of this Grid member in FQDN format."
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


class ZoneForwardForwardingServers(_DnsNested):
    """forwarding_servers list entry - per-member forwarding config.

    Each entry overrides the zone-level forward_to for a specific Grid member.
    The ``forward_to`` sub-list reuses the same ExtServer-compatible shape.
    """

    name: str | None = Field(
        default=None, description="The name of this Grid member in FQDN format."
    )
    forwarders_only: bool | None = Field(
        default=None,
        description="Determines if the appliance sends queries to forwarders only, and not to other internal or Internet root servers.",
    )
    forward_to: list[ExtServer] | None = Field(
        default=None,
        description="The information for the remote name servers to which you want the Infoblox appliance to forward queries for a specified domain name.",
    )
    use_override_forwarders: bool | None = Field(
        default=None, description="Use flag for: forward_to"
    )  # ---------------------------------------------------------------------------


# Main ZoneForward model
# ---------------------------------------------------------------------------


class ZoneForward(BaseModel):
    """NIOS forward DNS zone.

    All 31 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS` and stripped by :class:`ZoneForwardResource` on PUT.
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

    # --- forwarding config ---
    forward_to: list[ZoneForwardForwardTo] | None = Field(
        default=None,
        description="The information for the remote name servers to which you want the Infoblox appliance to forward queries for a specified domain name.",
    )
    forwarding_servers: list[ZoneForwardForwardingServers] | None = Field(
        default=None,
        description="The information for the Grid members to which you want the Infoblox appliance to forward queries for a specified domain name.",
    )
    forwarders_only: bool | None = Field(
        default=None,
        description="Determines if the appliance sends queries to forwarders only, and not to other internal or Internet root servers.",
    )
    disable_ns_generation: bool | None = Field(
        default=None,
        description="Determines whether a auto-generation of NS records in parent zone is disabled or not. When this is set to False, the auto-generation is enabled.",
    )
    external_ns_group: str | None = Field(
        default=None, description="A forward stub server name server group."
    )
    ns_group: str | None = Field(
        default=None, description="A forwarding member name server group."
    )
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

    # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- misc ---
    using_srg_associations: bool | None = Field(
        default=None,
        description="This is true if the zone is associated with a shared record group.",
    )  # RO
