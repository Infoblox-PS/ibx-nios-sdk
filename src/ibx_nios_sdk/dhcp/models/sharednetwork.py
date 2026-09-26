# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Sharednetwork - NIOS DHCP IPv4 shared network.

All 53 properties from ``components.schemas.Sharednetwork`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue, LogicFilterRule

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "dhcp_utilization",
        "dhcp_utilization_status",
        "dynamic_hosts",
        "ms_ad_user_data",
        "static_hosts",
        "total_hosts",
        "uuid",
    }
)


class Sharednetwork(BaseModel):
    """NIOS DHCP IPv4 shared network."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    authority: bool | None = Field(default=None, description="Authority for the shared network.")
    bootfile: str | None = Field(
        default=None,
        description="The bootfile name for the shared network. You can configure the DHCP server to support clients that use the boot file name option in their DHCPREQUEST messages.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The bootserver address for the shared network. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
    )
    comment: str | None = Field(
        default=None, description="Comment for the shared network, maximum 256 characters."
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="This field controls whether only the DHCP server is allowed to update DNS, regardless of the DHCP clients requests. Note that changes for this field take effect only if ddns_use_option81 is True.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DNS update Time to Live (TTL) value of a shared network object. The TTL is a 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    ddns_update_fixed_addresses: bool | None = Field(
        default=None,
        description="By default, the DHCP server does not update DNS when it allocates a fixed address to a client. You can configure the DHCP server to update the A and PTR records of a client with a fixed address. When this feature is enabled and the DHCP server adds A and PTR records for a fixed address, the DHCP server never discards the records.",
    )
    ddns_use_option81: bool | None = Field(
        default=None, description="The support for DHCP Option 81 at the shared network level."
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="If set to true, BOOTP settings are disabled and BOOTP requests will be denied.",
    )  # read-only
    dhcp_utilization: int | None = Field(
        default=None,
        description="The percentage of the total DHCP utilization of the networks belonging to the shared network multiplied by 1000. This is the percentage of the total number of available IP addresses from all the networks belonging to the shared network versus the total number of all IP addresses in all of the networks in the shared network.",
    )
    dhcp_utilization_status: Literal["FULL", "HIGH", "LOW", "NORMAL"] | str | None = Field(
        default=None,
        description="A string describing the utilization level of the shared network.",
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a shared network is disabled or not. When this is set to False, the shared network is enabled.",
    )  # read-only
    dynamic_hosts: int | None = Field(
        default=None, description="The total number of DHCP leases issued for the shared network."
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a shared network object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    ignore_client_identifier: bool | None = Field(
        default=None, description="If set to true, the client identifier will be ignored."
    )
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="If this field is set to False, the appliance returns all DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )
    ignore_id: Literal["NONE", "CLIENT", "MACADDR"] | str | None = Field(
        default=None,
        description='Indicates whether the appliance will ignore DHCP client IDs or MAC addresses. Valid values are "NONE", "CLIENT", or "MACADDR". The default is "NONE".',
    )
    ignore_mac_addresses: list[str] | None = Field(
        default=None, description="A list of MAC addresses the appliance will ignore."
    )
    lease_scavenge_time: int | None = Field(
        default=None,
        description="An integer that specifies the period of time (in seconds) that frees and backs up leases remained in the database before they are automatically deleted. To disable lease scavenging, set the parameter to -1. The minimum positive value must be greater than 86400 seconds (1 day).",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the this shared network. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )
    name: str | None = Field(default=None, description="The name of the IPv6 Shared Network.")
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which this shared network resides.",
    )
    networks: list[Any] | None = Field(
        default=None,
        description="A list of networks belonging to the shared network Each individual list item must be specified as an object containing a '_ref' parameter to a network reference, for example:: [{ \"_ref\": \"network/ZG5zLm5ldHdvcmskMTAuMwLvMTYvMA\", }] if the reference of the wanted network is not known, it is possible to specify search parameters for the network instead in the following way:: [{ \"_ref\": { 'network': '10.0.0.0/8', } }] note that in this case the search must match exactly one network for the assignment to be successful.",
    )
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address of the next server that the host needs to boot.",
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value of a shared network object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )  # read-only
    static_hosts: int | None = Field(
        default=None,
        description="The number of static DHCP addresses configured in the shared network.",
    )
    total_hosts: int | None = Field(
        default=None,
        description="The total number of DHCP addresses configured in the shared network.",
    )
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )
    use_authority: bool | None = Field(default=None, description="Use flag for: authority")
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_ddns_generate_hostname: bool | None = Field(
        default=None, description="Use flag for: ddns_generate_hostname"
    )
    use_ddns_ttl: bool | None = Field(default=None, description="Use flag for: ddns_ttl")
    use_ddns_update_fixed_addresses: bool | None = Field(
        default=None, description="Use flag for: ddns_update_fixed_addresses"
    )
    use_ddns_use_option81: bool | None = Field(
        default=None, description="Use flag for: ddns_use_option81"
    )
    use_deny_bootp: bool | None = Field(default=None, description="Use flag for: deny_bootp")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_ignore_client_identifier: bool | None = Field(
        default=None, description="Use flag for: ignore_client_identifier"
    )
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_ignore_id: bool | None = Field(default=None, description="Use flag for: ignore_id")
    use_lease_scavenge_time: bool | None = Field(
        default=None, description="Use flag for: lease_scavenge_time"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_nextserver: bool | None = Field(default=None, description="Use flag for: nextserver")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_pxe_lease_time: bool | None = Field(
        default=None, description="Use flag for: pxe_lease_time"
    )
    use_update_dns_on_lease_renewal: bool | None = Field(
        default=None, description="Use flag for: update_dns_on_lease_renewal"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
