# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Networkcontainer - NIOS IPAM IPv4 network container.

All 102 properties from ``components.schemas.Networkcontainer`` in the v2.14
IPAM swagger are represented here. Deeply nested types are typed as
``list[dict[str, Any]] | None`` or ``dict[str, Any] | None``.

NOTE: The following complex nested schemas are inlined as dicts:
  - NetworkcontainerCloudInfo
  - NetworkcontainerDiscoveryBasicPollSettings
  - NetworkcontainerDiscoveryBlackoutSetting
  - NetworkcontainerPortControlBlackoutSetting
  - NetworkcontainerIpamThresholdSettings
  - NetworkcontainerIpamTrapSettings
  - NetworkcontainerSubscribeSettings
  - NetworkcontainerResize (function schema)
  - NetworkcontainerNextAvailableNetwork (function schema)
  - NetworkcontainerMsAdUserData
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
        "discovery_engine_type",
        "endpoint_sources",
        "last_rir_registration_update_sent",
        "last_rir_registration_update_status",
        "mgm_private_overridable",
        "ms_ad_user_data",
        "network_container",
        "rir",
        "utilization",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Networkcontainer model
# ---------------------------------------------------------------------------


class Networkcontainer(BaseModel):
    """NIOS IPAM IPv4 network container.

    All 102 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- authority ---
    authority: bool | None = Field(
        default=None, description="Authority for the DHCP network container."
    )
    auto_create_reversezone: bool | None = Field(
        default=None,
        description="This flag controls whether reverse zones are automatically created when the network is added.",
    )  # --- BOOTP ---
    bootfile: str | None = Field(
        default=None,
        description="The boot server IPv4 Address or name in FQDN format for the network container. You can specify the name and/or IP address of the boot server that the host needs to boot.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The bootserver address for the network container. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
    )  # --- cloud info (complex nested - dict) ---
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common ---
    comment: str | None = Field(
        default=None, description="Comment for the network container; maximum 256 characters."
    )  # --- DDNS ---
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this network container.",
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server is allowed to update DNS, regardless of the DHCP client requests. Note that changes for this field take effect only if ddns_use_option81 is True.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DNS update Time to Live (TTL) value of a DHCP network container object. The TTL is a 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    ddns_update_fixed_addresses: bool | None = Field(
        default=None,
        description="By default, the DHCP server does not update DNS when it allocates a fixed address to a client. You can configure the DHCP server to update the A and PTR records of a client with a fixed address. When this feature is enabled and the DHCP server adds A and PTR records for a fixed address, the DHCP server never discards the records.",
    )
    ddns_use_option81: bool | None = Field(
        default=None, description="The support for DHCP Option 81 at the network container level."
    )  # --- deletion ---
    delete_reason: str | None = Field(
        default=None, description="The reason for deleting the RIR registration request."
    )  # --- DHCP ---
    deny_bootp: bool | None = Field(
        default=None,
        description="If set to True, BOOTP settings are disabled and BOOTP requests will be denied.",
    )  # --- read-only ---
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(
        default=None, description="Discover now status for this network container."
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
        default=None, description="The member that will run discovery for this network container."
    )  # --- email ---
    email_list: list[str] | None = Field(
        default=None,
        description="The e-mail lists to which the appliance sends DHCP threshold alarm e-mail messages.",
    )  # --- DDNS flags ---
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP network container object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_dhcp_thresholds: bool | None = Field(
        default=None,
        description="Determines if DHCP thresholds are enabled for the network container.",
    )
    enable_discovery: bool | None = Field(
        default=None,
        description="Determines whether a discovery is enabled or not for this network container. When this is set to False, the network container discovery is disabled.",
    )
    enable_email_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are sent through email."
    )
    enable_immediate_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the network container should be immediately enabled.",
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    enable_snmp_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are send through SNMP."
    )  # --- read-only ---
    endpoint_sources: list[dict[str, Any] | str] | None = Field(
        default=None,
        description="The endpoints that provides data for the DHCP Network Container object.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- realms ---
    federated_realms: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the federated realms associated to this network container.",
    )  # --- threshold settings ---
    high_water_mark: int | None = Field(
        default=None,
        description="The percentage of DHCP network container usage threshold above which network container usage is not expected and may warrant your attention. When the high watermark is reached, the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    high_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage of DHCP network container usage below which the corresponding SNMP trap is reset. A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The high watermark reset value must be lower than the high watermark value.",
    )  # --- DHCP options ---
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="If this field is set to False, the appliance returns all DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )
    ignore_id: Literal["NONE", "CLIENT", "MACADDR"] | str | None = Field(
        default=None,
        description="Indicates whether the appliance will ignore DHCP client IDs or MAC addresses.",
    )
    ignore_mac_addresses: list[str] | None = Field(
        default=None, description="A list of MAC addresses the appliance will ignore."
    )  # --- IPAM alerting ---
    ipam_email_addresses: list[str] | None = Field(
        default=None,
        description="The e-mail lists to which the appliance sends IPAM threshold alarm e-mail messages.",
    )
    ipam_threshold_settings: dict[str, Any] | None = Field(
        default=None, description="IPAM utilization-threshold trigger settings."
    )
    ipam_trap_settings: dict[str, Any] | None = Field(
        default=None, description="IPAM utilization SNMP-trap settings."
    )  # --- read-only ---
    last_rir_registration_update_sent: int | None = Field(
        default=None, description="The timestamp when the last RIR registration update was sent."
    )
    last_rir_registration_update_status: str | None = Field(
        default=None, description="Last RIR registration update status."
    )  # --- lease ---
    lease_scavenge_time: int | None = Field(
        default=None,
        description="An integer that specifies the period of time (in seconds) that frees and backs up leases remained in the database before they are automatically deleted. To disable lease scavenging, set the parameter to -1. The minimum positive value must be greater than 86400 seconds (1 day).",
    )  # --- logic filters ---
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the this network container. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )  # --- thresholds ---
    low_water_mark: int | None = Field(
        default=None,
        description="The percentage of DHCP network container usage below which the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    low_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage of DHCP network container usage threshold below which network container usage is not expected and may warrant your attention. When the low watermark is crossed, the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The low watermark reset value must be higher than the low watermark value.",
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
        description="The network address in IPv4 Address/CIDR format. For regular expression searches, only the IPv4 Address portion is supported. Searches for the CIDR portion is always an exact match. For example, both network containers 10.0.0.0/8 and 20.1.0.0/16 are matched by expression '.0' and only 20.1.0.0/16 is matched by '.0/16'.",
    )  # CIDR string or object

    # --- read-only ---
    network_container: str | None = Field(
        default=None, description="The network container to which this network belongs, if any."
    )  # --- network view ---
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this network resides."
    )  # --- function schema (not stored, used only in function calls) ---
    next_available_network: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the next-available-network operation."
    )  # --- nextserver ---
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address of the next server that the host needs to boot.",
    )  # --- DHCP options (complex nested - list of dicts) ---
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )  # --- port control blackout ---
    port_control_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Port-control blackout schedule for this object."
    )  # --- PXE ---
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value of a DHCP Network container object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )  # --- lease recycling ---
    recycle_leases: bool | None = Field(
        default=None,
        description="If the field is set to True, the leases are kept in the Recycle Bin until one week after expiration. Otherwise, the leases are permanently deleted.",
    )  # --- subnet removal ---
    remove_subnets: bool | None = Field(
        default=None,
        description="Remove subnets delete option. Determines whether all child objects should be removed alongside with the network container or child objects should be assigned to another parental container. By default child objects are deleted with the network container.",
    )  # --- resize (function schema) ---
    resize: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the resize-network operation."
    )  # --- DHCP restart ---
    restart_if_needed: bool | None = Field(
        default=None, description="Restarts the member service."
    )  # --- read-only ---
    rir: Literal["RIPE", "NONE"] | str | None = Field(
        default=None,
        description="The registry (RIR) that allocated the network container address space.",
    )  # --- RIR ---
    rir_organization: str | None = Field(
        default=None, description="The RIR organization associated with the network container."
    )
    rir_registration_action: Literal["NONE", "CREATE", "MODIFY", "DELETE"] | str | None = Field(
        default=None, description="The RIR registration action."
    )
    rir_registration_status: Literal["REGISTERED", "NOT_REGISTERED"] | str | None = Field(
        default=None, description="The registration status of the network container in RIR."
    )  # --- port control ---
    same_port_control_discovery_blackout: bool | None = Field(
        default=None,
        description="If the field is set to True, the discovery blackout setting will be used for port control blackout setting.",
    )
    send_rir_request: bool | None = Field(
        default=None, description="Determines whether to send the RIR registration request."
    )  # --- subscribe settings ---
    subscribe_settings: dict[str, Any] | None = Field(
        default=None,
        description="Subscription settings for receiving updates from upstream sources.",
    )  # --- unmanaged ---
    unmanaged: bool | None = Field(
        default=None, description="Determines whether the network container is unmanaged or not."
    )  # --- DNS on renewal ---
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )  # --- use flags ---
    use_authority: bool | None = Field(default=None, description="Use flag for: authority")
    use_blackout_setting: bool | None = Field(
        default=None,
        description="Use flag for: discovery_blackout_setting , port_control_blackout_setting, same_port_control_discovery_blackout",
    )
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
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
    use_discovery_basic_polling_settings: bool | None = Field(
        default=None, description="Use flag for: discovery_basic_poll_settings"
    )
    use_email_list: bool | None = Field(default=None, description="Use flag for: email_list")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_enable_dhcp_thresholds: bool | None = Field(
        default=None, description="Use flag for: enable_dhcp_thresholds"
    )
    use_enable_discovery: bool | None = Field(
        default=None, description="Use flag for: discovery_member , enable_discovery"
    )
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_ignore_id: bool | None = Field(default=None, description="Use flag for: ignore_id")
    use_ipam_email_addresses: bool | None = Field(
        default=None, description="Use flag for: ipam_email_addresses"
    )
    use_ipam_threshold_settings: bool | None = Field(
        default=None, description="Use flag for: ipam_threshold_settings"
    )
    use_ipam_trap_settings: bool | None = Field(
        default=None, description="Use flag for: ipam_trap_settings"
    )
    use_lease_scavenge_time: bool | None = Field(
        default=None, description="Use flag for: lease_scavenge_time"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_mgm_private: bool | None = Field(default=None, description="Use flag for: mgm_private")
    use_nextserver: bool | None = Field(default=None, description="Use flag for: nextserver")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_pxe_lease_time: bool | None = Field(
        default=None, description="Use flag for: pxe_lease_time"
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
    use_zone_associations: bool | None = Field(
        default=None, description="Use flag for: zone_associations"
    )  # --- read-only ---
    utilization: int | None = Field(
        default=None, description="The network container utilization in percentage."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- zone associations ---
    zone_associations: list[dict[str, Any]] | None = Field(
        default=None, description="The list of zones associated with this network."
    )
