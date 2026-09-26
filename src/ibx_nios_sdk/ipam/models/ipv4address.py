# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv4address - NIOS IPAM IPv4 address object.

All 23 properties from ``components.schemas.Ipv4address`` in the v2.14 IPAM
swagger are represented here. This object is primarily read-only (aggregate
current IP state populated by NIOS); the only writable fields are
``extattrs`` and ``discovered_data``.

NOTE: The following complex nested schemas are inlined as dicts:
  - Ipv4addressDiscoveredData (96+ read-only discovery fields)
  - Ipv4addressMsAdUserData
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
        "dhcp_client_identifier",
        "discover_now_status",
        "discovered_data",
        "fingerprint",
        "ip_address",
        "is_conflict",
        "is_invalid_mac",
        "lease_state",
        "mac_address",
        "ms_ad_user_data",
        "names",
        "network",
        "network_view",
        "objects",
        "reserved_port",
        "status",
        "types",
        "usage",
        "username",
    }
)


# ---------------------------------------------------------------------------
# Main Ipv4address model
# ---------------------------------------------------------------------------


class Ipv4address(BaseModel):
    """NIOS IPAM IPv4 address object.

    All 23 swagger properties are present. Almost all fields are read-only
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
    dhcp_client_identifier: str | None = Field(
        default=None, description="The client unique identifier."
    )
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(
        default=None, description="Discover now status for this address."
    )  # --- discovery data (complex nested - dict) ---
    discovered_data: dict[str, Any] | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )  # --- extended attributes (writable) ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- read-only ---
    fingerprint: str | None = Field(default=None, description="DHCP fingerprint for the address.")
    ip_address: str | None = Field(default=None, description="The IP address.")
    is_conflict: bool | None = Field(
        default=None,
        description="If set to True, the IP address has either a MAC address conflict or a DHCP lease conflict detected through a network discovery.",
    )
    is_invalid_mac: bool | None = Field(
        default=None,
        description="This flag reflects whether the MAC address for this address is invalid.",
    )
    lease_state: str | None = Field(default=None, description="The lease state of the address.")
    mac_address: str | None = Field(
        default=None, description="The MAC address."
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
    status: str | None = Field(default=None, description="The current status of the address.")
    types: list[str] | None = Field(
        default=None,
        description="The types of associated objects. This field supports both single and array search.",
    )
    usage: list[str] | None = Field(
        default=None,
        description="Indicates whether the IP address is configured for DNS or DHCP. This field supports both single and array search.",
    )
    username: str | None = Field(
        default=None,
        description='The name of the user who created or modified the record. The "username" field is populated only for lease objects that have a MAC Address Filter configured with user details.',
    )
