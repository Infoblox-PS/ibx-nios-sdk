# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6network - NIOS IPAM IPv6 network.

All 88 properties from ``components.schemas.Ipv6network`` in the v2.14 IPAM
swagger are represented here. Deeply nested types (cloud info, members, discovery
settings, etc.) are typed as ``list[dict[str, Any]] | None`` or
``dict[str, Any] | None``.

NOTE: The following complex nested schemas are inlined as dicts:
  - Ipv6networkCloudInfo
  - Ipv6networkDiscoveryBasicPollSettings
  - Ipv6networkDiscoveryBlackoutSetting
  - Ipv6networkPortControlBlackoutSetting
  - Ipv6networkSubscribeSettings
  - Ipv6networkMsAdUserData
  - Ipv6networkExpandNetwork (function schema, not stored)
  - Ipv6networkNextAvailableIp (function schema, not stored)
  - Ipv6networkNextAvailableNetwork (function schema, not stored)
  - Ipv6networkNextAvailableVlan (function schema, not stored)
  - Ipv6networkSplitNetwork (function schema, not stored)
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
        "discover_now_status",
        "discovered_bgp_as",
        "discovered_vlan_id",
        "discovered_vlan_name",
        "discovered_vrf_description",
        "discovered_vrf_name",
        "discovered_vrf_rd",
        "discovery_engine_type",
        "endpoint_sources",
        "last_rir_registration_update_sent",
        "last_rir_registration_update_status",
        "mgm_private_overridable",
        "ms_ad_user_data",
        "network_container",
        "rir",
        "unmanaged_count",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Ipv6network model
# ---------------------------------------------------------------------------


class Ipv6network(BaseModel):
    """NIOS IPAM IPv6 network.

    All 88 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- auto reverse zone ---
    auto_create_reversezone: bool | None = Field(
        default=None,
        description="This flag controls whether reverse zones are automatically created when the network is added.",
    )  # --- cloud info (complex nested - dict) ---
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common ---
    comment: str | None = Field(
        default=None, description="Comment for the network; maximum 256 characters."
    )  # --- DDNS ---
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this network.",
    )
    ddns_enable_option_fqdn: bool | None = Field(
        default=None,
        description="Use this method to set or retrieve the ddns_enable_option_fqdn flag of a DHCP IPv6 Network object. This method controls whether the FQDN option sent by the client is to be used, or if the server can automatically generate the FQDN. This setting overrides the upper-level settings.",
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="This field controls whether only the DHCP server is allowed to update DNS, regardless of the DHCP clients requests. Note that changes for this field take effect only if ddns_enable_option_fqdn is True.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DNS update Time to Live (TTL) value of a DHCP network object. The TTL is a 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )  # --- deletion ---
    delete_reason: str | None = Field(
        default=None, description="The reason for deleting the RIR registration request."
    )  # --- state ---
    disable: bool | None = Field(
        default=None,
        description="Determines whether a network is disabled or not. When this is set to False, the network is enabled.",
    )  # --- read-only ---
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(default=None, description="Discover now status for this network.")
    discovered_bgp_as: str | None = Field(
        default=None,
        description='Number of the discovered BGP AS. When multiple BGP autonomous systems are discovered in the network, this field displays "Multiple".',
    )  # --- discovered data (writable) ---
    discovered_bridge_domain: str | None = Field(
        default=None, description="Discovered bridge domain."
    )
    discovered_tenant: str | None = Field(
        default=None, description="Discovered tenant."
    )  # --- read-only ---
    discovered_vlan_id: str | None = Field(
        default=None,
        description='The identifier of the discovered VLAN. When multiple VLANs are discovered in the network, this field displays "Multiple".',
    )
    discovered_vlan_name: str | None = Field(
        default=None,
        description='The name of the discovered VLAN. When multiple VLANs are discovered in the network, this field displays "Multiple".',
    )
    discovered_vrf_description: str | None = Field(
        default=None,
        description='Description of the discovered VRF. When multiple VRFs are discovered in the network, this field displays "Multiple".',
    )
    discovered_vrf_name: str | None = Field(
        default=None,
        description='The name of the discovered VRF. When multiple VRFs are discovered in the network, this field displays "Multiple".',
    )
    discovered_vrf_rd: str | None = Field(
        default=None,
        description='Route distinguisher of the discovered VRF. When multiple VRFs are discovered in the network, this field displays "Multiple".',
    )  # --- discovery settings (complex nested - dict) ---
    discovery_basic_poll_settings: dict[str, Any] | None = Field(
        default=None, description="Basic discovery polling settings."
    )
    discovery_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Discovery blackout schedule for this object."
    )  # --- read-only ---
    discovery_engine_type: (
        Literal["NETMRI", "VDISCOVERY", "NETWORK_INSIGHT", "UNKNOWN", "NONE"] | str | None
    ) = Field(
        default=None, description="The network discovery engine type."
    )  # --- discovery member ---
    discovery_member: str | None = Field(
        default=None, description="The member that will run discovery for this network."
    )  # --- IPv6 DNS ---
    domain_name: str | None = Field(
        default=None,
        description="Use this method to set or retrieve the domain_name value of a DHCP IPv6 Network object.",
    )
    domain_name_servers: list[str] | None = Field(
        default=None,
        description="Use this method to set or retrieve the dynamic DNS updates flag of a DHCP IPv6 Network object. The DHCP server can send DDNS updates to DNS servers in the same Grid and to external DNS servers. This setting overrides the member level settings.",
    )  # --- DDNS flags ---
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP IPv6 network object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_discovery: bool | None = Field(
        default=None,
        description="Determines whether a discovery is enabled or not for this network. When this is set to False, the network discovery is disabled.",
    )
    enable_ifmap_publishing: bool | None = Field(
        default=None, description="Determines if IFMAP publishing is enabled for the network."
    )
    enable_immediate_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the network should be immediately enabled.",
    )  # --- read-only ---
    endpoint_sources: list[dict[str, Any] | str] | None = Field(
        default=None,
        description="The endpoints that provides data for the DHCP IPv6 Network object.",
    )  # --- function schemas (not stored as fields) ---
    expand_network: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the expand-network operation."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- realms ---
    federated_realms: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the federated realms associated to this network",
    )  # --- read-only ---
    last_rir_registration_update_sent: int | None = Field(
        default=None, description="The timestamp when the last RIR registration update was sent."
    )
    last_rir_registration_update_status: str | None = Field(
        default=None, description="Last RIR registration update status."
    )  # --- logic filters ---
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on this IPv6 network. This list corresponds to the match rules that are written to the DHCPv6 configuration file.",
    )  # --- members (complex nested - list of dicts) ---
    members: list[dict[str, Any]] | None = Field(
        default=None,
        description='A list of members servers that serve DHCP for the network. All members in the array must be of the same type. The struct type must be indicated in each element, by setting the "_struct" member to the struct type.',
    )  # --- private cloud management ---
    mgm_private: bool | None = Field(
        default=None,
        description="This field controls whether this object is synchronized with the Multi-Grid Master. If this field is set to True, objects are not synchronized.",
    )  # --- read-only ---
    mgm_private_overridable: bool | None = Field(
        default=None,
        description="This field is assumed to be True unless filled by any conforming objects, such as Network, IPv6 Network, Network Container, IPv6 Network Container, and Network View. This value is set to False if mgm_private is set to True in the parent object.",
    )  # --- MS AD user data (complex nested - dict) ---
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- network identity ---
    network: Any | None = Field(
        default=None,
        description="The network address in IPv6 Address/CIDR format. For regular expression searches, only the IPv6 Address portion is supported. Searches for the CIDR portion is always an exact match. For example, both network containers 16::0/28 and 26::0/24 are matched by expression '.6' and only 26::0/24 is matched by '.6/24'.",
    )  # IPv6 CIDR string or object

    # --- read-only ---
    network_container: str | None = Field(
        default=None, description="The network container to which this network belongs, if any."
    )  # --- network view ---
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this network resides."
    )  # --- function schemas (not stored, used only in function calls) ---
    next_available_ip: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the next-available-IP operation."
    )
    next_available_network: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the next-available-network operation."
    )
    next_available_vlan: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the next-available-VLAN operation."
    )  # --- DHCP options (complex nested - list of dicts) ---
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )  # --- port control blackout ---
    port_control_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Port-control blackout schedule for this object."
    )  # --- IPv6 DHCP lifetimes ---
    preferred_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the preferred lifetime value of a DHCP IPv6 Network object.",
    )  # --- lease recycling ---
    recycle_leases: bool | None = Field(
        default=None,
        description="If the field is set to True, the leases are kept in the Recycle Bin until one week after expiration. Otherwise, the leases are permanently deleted.",
    )  # --- DHCP restart ---
    restart_if_needed: bool | None = Field(
        default=None, description="Restarts the member service."
    )  # --- read-only ---
    rir: Literal["RIPE", "NONE"] | str | None = Field(
        default=None,
        description="The registry (RIR) that allocated the IPv6 network address space.",
    )  # --- RIR ---
    rir_organization: str | None = Field(
        default=None, description="The RIR organization associated with the IPv6 network."
    )
    rir_registration_action: Literal["NONE", "CREATE", "MODIFY", "DELETE"] | str | None = Field(
        default=None, description="The RIR registration action."
    )
    rir_registration_status: Literal["REGISTERED", "NOT_REGISTERED"] | str | None = Field(
        default=None, description="The registration status of the IPv6 network in RIR."
    )  # --- port control ---
    same_port_control_discovery_blackout: bool | None = Field(
        default=None,
        description="If the field is set to True, the discovery blackout setting will be used for port control blackout setting.",
    )
    send_rir_request: bool | None = Field(
        default=None, description="Determines whether to send the RIR registration request."
    )  # --- split network (function schema) ---
    split_network: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the split-network operation."
    )  # --- subscribe settings ---
    subscribe_settings: dict[str, Any] | None = Field(
        default=None,
        description="Subscription settings for receiving updates from upstream sources.",
    )  # --- template ---
    template: str | None = Field(
        default=None,
        description="If set on creation, the network is created according to the values specified in the selected template.",
    )  # --- unmanaged ---
    unmanaged: bool | None = Field(
        default=None, description="Determines whether the DHCP IPv6 Network is unmanaged or not."
    )  # --- read-only ---
    unmanaged_count: int | None = Field(
        default=None,
        description="The number of unmanaged IP addresses as discovered by network discovery.",
    )  # --- DNS on renewal ---
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )  # --- use flags ---
    use_blackout_setting: bool | None = Field(
        default=None,
        description="Use flag for: discovery_blackout_setting , port_control_blackout_setting, same_port_control_discovery_blackout",
    )
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_ddns_enable_option_fqdn: bool | None = Field(
        default=None, description="Use flag for: ddns_enable_option_fqdn"
    )
    use_ddns_generate_hostname: bool | None = Field(
        default=None, description="Use flag for: ddns_generate_hostname"
    )
    use_ddns_ttl: bool | None = Field(default=None, description="Use flag for: ddns_ttl")
    use_discovery_basic_polling_settings: bool | None = Field(
        default=None, description="Use flag for: discovery_basic_poll_settings"
    )
    use_domain_name: bool | None = Field(default=None, description="Use flag for: domain_name")
    use_domain_name_servers: bool | None = Field(
        default=None, description="Use flag for: domain_name_servers"
    )
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_enable_discovery: bool | None = Field(
        default=None, description="Use flag for: discovery_member , enable_discovery"
    )
    use_enable_ifmap_publishing: bool | None = Field(
        default=None, description="Use flag for: enable_ifmap_publishing"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_mgm_private: bool | None = Field(default=None, description="Use flag for: mgm_private")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_recycle_leases: bool | None = Field(
        default=None, description="Use flag for: recycle_leases"
    )
    use_subscribe_settings: bool | None = Field(
        default=None, description="Use flag for: subscribe_settings"
    )
    use_update_dns_on_lease_renewal: bool | None = Field(
        default=None, description="Use flag for: update_dns_on_lease_renewal"
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )
    use_zone_associations: bool | None = Field(
        default=None, description="Use flag for: zone_associations"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- IPv6 DHCP lifetime ---
    valid_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the valid lifetime value of a DHCP IPv6 Network object.",
    )  # --- VLANs ---
    vlans: list[dict[str, Any]] | None = Field(
        default=None, description="List of VLANs assigned to Network."
    )  # --- zone associations ---
    zone_associations: list[dict[str, Any]] | None = Field(
        default=None, description="The list of zones associated with this network."
    )
