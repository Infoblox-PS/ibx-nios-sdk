# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostIpv6addr - NIOS DNS host record IPv6 address sub-object.

All 31 properties from ``components.schemas.RecordHostIpv6addr`` in the
v2.14 DNS swagger are represented here.

This model is used both as the element type for ``RecordHost.ipv6addrs``
and as the standalone ``record:host_ipv6addr`` resource.

Deep nested types (``RecordHostIpv6addrDiscoveredData``,
``RecordHostIpv6addrMsAdUserData``) are approximated as
``dict[str, Any] | None``.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "discover_now_status",
        "discovered_data",
        "host",
        "last_queried",
        "ms_ad_user_data",
        "network",
        "network_view",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main RecordHostIpv6addr model
# ---------------------------------------------------------------------------


class RecordHostIpv6addr(BaseModel):
    """NIOS host record IPv6 address entry.

    All 31 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.

    Deep nested discovery / MS-AD fields are typed as ``dict[str, Any] | None``
    (see ``dns/NOTES.md`` approximations section).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- DHCPv6 address type ---
    address_type: Literal["ADDRESS", "PREFIX", "BOTH"] | str | None = Field(
        default=None, description="Type of the DHCP IPv6 Host Address object."
    )  # --- DHCPv6 configuration ---
    configure_for_dhcp: bool | None = Field(
        default=None,
        description="Set this to True to enable the DHCP configuration for this IPv6 host address.",
    )  # --- read-only ---
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(
        default=None, description="The discovery status of this IPv6 Host Address."
    )  # --- discovery data (approximated) ---
    discovered_data: dict[str, Any] | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )  # --- DHCPv6 domain ---
    domain_name: str | None = Field(
        default=None,
        description="Use this method to set or retrieve the domain_name value of the DHCP IPv6 Host Address object.",
    )
    domain_name_servers: list[str] | None = Field(
        default=None,
        description="The IPv6 addresses of DNS recursive name servers to which the DHCP client can send name resolution requests. The DHCP server includes this information in the DNS Recursive Name Server option in Advertise, Rebind, Information-Request, and Reply messages.",
    )  # --- DHCPv6 DUID ---
    duid: str | None = Field(
        default=None, description="DHCPv6 Unique Identifier (DUID) of the address object."
    )  # --- read-only ---
    host: str | None = Field(
        default=None,
        description="The host to which the IPv6 host address belongs, in FQDN format. It is only present when the host address object is not returned as part of a host.",
    )  # --- core identity ---
    ipv6addr: str | None = Field(
        default=None, description="The IPv6 Address prefix of the DHCP IPv6 Host Address object."
    )  # --- DHCPv6 prefix ---
    ipv6prefix: str | None = Field(
        default=None, description="The IPv6 Address prefix of the DHCP IPv6 Host Address object."
    )
    ipv6prefix_bits: int | None = Field(
        default=None, description="Prefix bits of the DHCP IPv6 Host Address object."
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- DHCP logic filters ---
    logic_filter_rules: list[Any] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the this host address. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )  # --- DHCPv6 MAC / match ---
    mac: str | None = Field(default=None, description="The MAC address for this host address.")
    match_client: Literal["DUID", "MAC_ADDRESS"] | str | None = Field(
        default=None,
        description='The match_client value for this fixed address. Valid values are: "DUID": The host IP address is leased to the matching DUID. "MAC_ADDRESS": The host IP address is leased to the matching MAC address.',
    )  # --- MS AD user data (approximated) ---
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- read-only ---
    network: str | None = Field(
        default=None, description="The network of the host address, in FQDN/CIDR format."
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which the host address resides."
    )  # --- DHCPv6 options ---
    options: list[Any] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )  # --- DHCPv6 lifetime ---
    preferred_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the preferred lifetime value of the DHCP IPv6 Host Address object.",
    )  # --- reserved interface ---
    reserved_interface: str | None = Field(
        default=None,
        description="The reference to the reserved interface to which the device belongs.",
    )  # --- use flags ---
    use_domain_name: bool | None = Field(default=None, description="Use flag for: domain_name")
    use_domain_name_servers: bool | None = Field(
        default=None, description="Use flag for: domain_name_servers"
    )
    use_for_ea_inheritance: bool | None = Field(
        default=None,
        description="Set this to True when using this host address for EA inheritance.",
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- DHCPv6 lifetime ---
    valid_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the valid lifetime value of the DHCP IPv6 Host Address object.",
    )
