# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHost - NIOS DNS host record.

All 38 properties from ``components.schemas.RecordHost`` in the v2.14 DNS
swagger are represented here.

The ``ipv4addrs`` and ``ipv6addrs`` fields use the same model types as the
standalone ``record:host_ipv4addr`` and ``record:host_ipv6addr`` WAPI objects,
imported from their own model files to avoid duplication.

Deep nested types (``RecordHostCloudInfo``, ``RecordHostSnmp3Credential``,
``RecordHostSnmpCredential``, ``RecordHostMsAdUserData``) that are unique to
RecordHost and have no reuse outside this object are approximated as
``dict[str, Any] | None``.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.dns.models.record_host_ipv4addr import RecordHostIpv4addr
from ibx_nios_sdk.dns.models.record_host_ipv6addr import RecordHostIpv6addr

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "creation_time",
        "dns_name",
        "last_queried",
        "ms_ad_user_data",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main RecordHost model
# ---------------------------------------------------------------------------


class RecordHost(BaseModel):
    """NIOS DNS host record.

    All 38 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.

    The ``ipv4addrs`` field is ``list[RecordHostIpv4addr] | None`` - typed,
    not raw dicts - so callers get fully-typed address objects.

    Credential / CloudInfo nested objects are approximated as
    ``dict[str, Any] | None`` (see ``dns/NOTES.md`` approximations section).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- DNS aliases ---
    aliases: list[str] | None = Field(
        default=None,
        description="This is a list of aliases for the host. The aliases must be in FQDN format. This value can be in unicode format.",
    )
    allow_telnet: bool | None = Field(
        default=None,
        description="This field controls whether the credential is used for both the Telnet and SSH credentials. If set to False, the credential is used only for SSH.",
    )  # --- device management credentials (approximated) ---
    cli_credentials: list[Any] | None = Field(
        default=None, description="The CLI credentials for the host record."
    )  # --- cloud info (approximated - RecordHostCloudInfo has same 8-field shape) ---
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common ---
    comment: str | None = Field(
        default=None, description="Comment for the record; maximum 256 characters."
    )
    configure_for_dns: bool | None = Field(
        default=None,
        description="When configure_for_dns is false, the host does not have parent zone information.",
    )  # --- read-only ---
    creation_time: int | None = Field(
        default=None, description="The time of the record creation in Epoch seconds format."
    )  # --- DDNS ---
    ddns_protected: bool | None = Field(
        default=None,
        description="Determines if the DDNS updates for this record are allowed or not.",
    )  # --- device tracking ---
    device_description: str | None = Field(
        default=None, description="The description of the device."
    )
    device_location: str | None = Field(default=None, description="The location of the device.")
    device_type: str | None = Field(default=None, description="The type of the device.")
    device_vendor: str | None = Field(
        default=None, description="The vendor of the device."
    )  # --- record state ---
    disable: bool | None = Field(
        default=None,
        description="Determines if the record is disabled or not. False means that the record is enabled.",
    )
    disable_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the record is disabled or not. False means that the discovery is enabled.",
    )  # --- read-only computed ---
    dns_aliases: list[str] | None = Field(
        default=None, description="The list of aliases for the host in punycode format."
    )
    dns_name: str | None = Field(
        default=None, description="The name for a host record in punycode format."
    )  # --- discovery ---
    enable_immediate_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the record should be immediately enabled.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- nested address lists (typed) ---
    ipv4addrs: list[RecordHostIpv4addr] | None = Field(
        default=None, description="This is a list of IPv4 Addresses for the host."
    )
    ipv6addrs: list[RecordHostIpv6addr] | None = Field(
        default=None, description="This is a list of IPv6 Addresses for the host."
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- MS AD user data (approximated) ---
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The host name in FQDN format This value can be in unicode format. Regular expression search is not supported for unicode values.",
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which the host record resides."
    )  # --- DDNS ---
    restart_if_needed: bool | None = Field(
        default=None, description="Restarts the member service."
    )
    rrset_order: str | None = Field(
        default=None,
        description='The value of this field specifies the order in which resource record sets are returned. The possible values are "cyclic", "random" and "fixed".',
    )  # --- SNMP credentials (approximated) ---
    snmp3_credential: dict[str, Any] | None = Field(
        default=None, description="SNMPv3 credential used to manage this object."
    )
    snmp_credential: dict[str, Any] | None = Field(
        default=None, description="SNMP (v1/v2c) credential used to manage this object."
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for record. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
    )  # --- use flags ---
    use_cli_credentials: bool | None = Field(
        default=None,
        description="If set to true, the CLI credential will override member-level settings.",
    )
    use_dns_ea_inheritance: bool | None = Field(
        default=None,
        description="When use_dns_ea_inheritance is True, the EA is inherited from associated zone.",
    )
    use_snmp3_credential: bool | None = Field(
        default=None,
        description="Determines if the SNMPv3 credential should be used for the record.",
    )
    use_snmp_credential: bool | None = Field(
        default=None,
        description="If set to true, the SNMP credential will override member-level settings.",
    )
    use_ttl: bool | None = Field(
        default=None, description="Use flag for: ttl"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- view / zone ---
    view: str | None = Field(
        default=None,
        description='The name of the DNS view in which the record resides. Example: "external".',
    )  # --- read-only ---
    zone: str | None = Field(
        default=None,
        description='The name of the zone in which the record resides. Example: "zone.com". If a view is not specified when searching by zone, the default view is used.',
    )
