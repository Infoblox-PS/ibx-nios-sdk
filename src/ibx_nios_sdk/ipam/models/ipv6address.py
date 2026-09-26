# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6address - NIOS IPAM IPv6 address object.

All 20 properties from ``components.schemas.Ipv6address`` in the v2.14 IPAM
swagger are represented here. This object is primarily read-only (aggregate
current IP state populated by NIOS); the only writable fields are
``extattrs`` and ``discovered_data``.

NOTE: The following complex nested schemas are inlined as dicts:
  - Ipv6addressDiscoveredData (read-only discovery fields)
  - Ipv6addressMsAdUserData
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "conflict_types",
        "discover_now_status",
        "discovered_data",
        "duid",
        "fingerprint",
        "ip_address",
        "is_conflict",
        "lease_state",
        "ms_ad_user_data",
        "names",
        "network",
        "network_view",
        "objects",
        "reserved_port",
        "status",
        "types",
        "usage",
    }
)


# ---------------------------------------------------------------------------
# Main Ipv6address model
# ---------------------------------------------------------------------------


class Ipv6address(BaseModel):
    """NIOS IPAM IPv6 address object.

    All 20 swagger properties are present. Almost all fields are read-only
    (populated by NIOS from DHCP leases, DNS records, and discovery).
    Read-only fields are collected in :data:`READONLY_FIELDS`.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    comment: str | None = Field(
        default=None, description="Comment for the address; maximum 256 characters."
    )
    conflict_types: (
        list[
            Literal[
                "MAC_ADDRESS",
                "DHCP_RANGE",
                "DUID",
                "RESERVED_PORT",
                "USED_RESERVED_PORT",
                "DEVICE_VENDOR",
                "DEVICE_TYPE",
                "VM_AFFILIATION",
                "NONE",
            ]
            | str
        ]
        | None
    ) = Field(default=None, description="Types of the conflict.")
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(
        default=None, description="Discover now status for this address."
    )  # --- discovery data (complex nested - dict) ---
    discovered_data: dict[str, Any] | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )  # --- read-only ---
    duid: str | None = Field(
        default=None, description="DHCPv6 Unique Identifier (DUID) of the address object."
    )  # --- extended attributes (writable) ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- read-only ---
    fingerprint: str | None = Field(default=None, description="DHCP fingerprint for the address.")
    ip_address: str | None = Field(
        default=None, description="IPv6 addresses of the address object."
    )
    is_conflict: bool | None = Field(
        default=None,
        description="IP address has either a duid conflict or a DHCP lease conflict detected through a network discovery.",
    )
    lease_state: str | None = Field(
        default=None, description="The lease state of the address."
    )  # --- MS AD user data (complex nested - dict) ---
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- read-only ---
    names: list[str] | None = Field(
        default=None,
        description="The DNS names. For example, if the IP address belongs to a host record, this field contains the hostname. This field supports both single and array search.",
    )
    network: str | None = Field(
        default=None, description="The network to which this address belongs, in FQDN/CIDR format."
    )
    network_view: str | None = Field(default=None, description="The name of the network view.")
    objects: str | None = Field(
        default=None, description="The objects associated with the IP address."
    )
    reserved_port: str | None = Field(
        default=None, description="The reserved port for the address."
    )
    status: Literal["USED", "UNUSED"] | str | None = Field(
        default=None, description="The current status of the address."
    )
    types: list[str] | None = Field(
        default=None,
        description="The types of associated objects. This field supports both single and array search.",
    )
    usage: list[str] | None = Field(
        default=None,
        description="Indicates whether the IP address is configured for DNS or DHCP. This field supports both single and array search.",
    )
