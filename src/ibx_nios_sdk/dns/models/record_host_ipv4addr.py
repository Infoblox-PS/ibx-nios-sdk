# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostIpv4addr - NIOS DNS host record IPv4 address sub-object.

All 33 properties from ``components.schemas.RecordHostIpv4addr`` in the
v2.14 DNS swagger are represented here.

This model is used both as the element type for ``RecordHost.ipv4addrs``
and as the standalone ``record:host_ipv4addr`` resource.

Deep nested types (``RecordHostIpv4addrDiscoveredData``,
``RecordHostIpv4addrMsAdUserData``) are approximated as
``dict[str, Any] | None`` - their shapes are identical in structure to
the equivalent RecordA discovery types but are formally separate schemas.
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
        "is_invalid_mac",
        "last_queried",
        "ms_ad_user_data",
        "network",
        "network_view",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main RecordHostIpv4addr model
# ---------------------------------------------------------------------------


class RecordHostIpv4addr(BaseModel):
    """NIOS host record IPv4 address entry.

    All 33 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.

    Deep nested discovery / MS-AD fields are typed as ``dict[str, Any] | None``
    (see ``dns/NOTES.md`` approximations section).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- DHCP boot options ---
    bootfile: str | None = Field(
        default=None, description="The name of the boot file the client must download."
    )
    bootserver: str | None = Field(
        default=None,
        description="The IP address or hostname of the boot file server where the boot file is stored.",
    )  # --- DHCP configuration ---
    configure_for_dhcp: bool | None = Field(
        default=None,
        description="Set this to True to enable the DHCP configuration for this host address.",
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="Set this to True to disable the BOOTP settings and deny BOOTP boot requests.",
    )  # --- read-only ---
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(
        default=None, description="The discovery status of this Host Address."
    )  # --- discovery data (approximated) ---
    discovered_data: dict[str, Any] | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )  # --- DHCP PXE ---
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients. You can specify the duration of time it takes a host to connect to a boot server, such as a TFTP server, and download the file it needs to boot. For example, set a longer lease time if the client downloads an OS (operating system) or configuration file, or set a shorter lease time if the client downloads only configuration changes. Enter the lease time for the preboot execution environment for hosts to boot remotely from a server.",
    )  # --- read-only ---
    host: str | None = Field(
        default=None,
        description="The host to which the host address belongs, in FQDN format. It is only present when the host address object is not returned as part of a host.",
    )  # --- use flags ---
    ignore_client_requested_options: bool | None = Field(
        default=None,
        description="If this field is set to false, the appliance returns all DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )  # --- core identity ---
    ipv4addr: str | None = Field(
        default=None, description="The IPv4 Address of the host."
    )  # --- read-only ---
    is_invalid_mac: bool | None = Field(
        default=None,
        description="This flag reflects whether the MAC address for this host address is invalid.",
    )
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- DHCP logic filters ---
    logic_filter_rules: list[Any] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the this host address. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )  # --- DHCP MAC ---
    mac: str | None = Field(default=None, description="The MAC address for this host address.")
    match_client: str | None = Field(
        default=None,
        description="Set this to 'MAC_ADDRESS' to assign the IP address to the selected host, provided that the MAC address of the requesting host matches the MAC address that you specify in the field. Set this to 'RESERVED' to reserve this particular IP address for future use, or if the IP address is statically configured on a system (the Infoblox server does not assign the address from a DHCP request).",
    )  # --- MS AD user data (approximated) ---
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- read-only ---
    network: str | None = Field(
        default=None, description="The network of the host address, in FQDN/CIDR format."
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which the host address resides."
    )  # --- DHCP next server ---
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN format and/or IPv4 Address of the next server that the host needs to boot.",
    )  # --- DHCP options ---
    options: list[Any] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )  # --- DHCP PXE lease ---
    pxe_lease_time: int | None = Field(
        default=None,
        description="The lease time for PXE clients, see *enable_pxe_lease_time* for more information.",
    )  # --- reserved interface ---
    reserved_interface: str | None = Field(
        default=None,
        description="The reference to the reserved interface to which the device belongs.",
    )  # --- use flags ---
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_deny_bootp: bool | None = Field(default=None, description="Use flag for: deny_bootp")
    use_for_ea_inheritance: bool | None = Field(
        default=None,
        description="Set this to True when using this host address for EA inheritance.",
    )
    use_ignore_client_requested_options: bool | None = Field(
        default=None, description="Use flag for: ignore_client_requested_options"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_nextserver: bool | None = Field(default=None, description="Use flag for: nextserver")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_pxe_lease_time: bool | None = Field(
        default=None, description="Use flag for: pxe_lease_time"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
