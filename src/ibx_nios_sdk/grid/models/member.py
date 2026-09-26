# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Member - NIOS Grid member.

All properties from ``components.schemas.Member`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "active_position",
        "is_dscp_capable",
        "is_master",
        "mmdb_ea_build_time",
        "mmdb_geoip_build_time",
        "service_status",
        "support_access_info",
        "uuid",
    }
)


class Member(BaseModel):
    """NIOS Grid member."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    active_position: str | None = Field(
        default=None, description="The active server of a Grid member."
    )
    additional_ip_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The additional IP list of a Grid member. This list contains additional interface information that can be used at the member level. Note that interface structure(s) with interface type set to 'MGMT' are not supported.",
    )
    automated_traffic_capture_setting: dict[str, Any] | None = Field(
        default=None, description="Settings controlling automated DNS traffic capture."
    )
    bgp_as: list[dict[str, Any]] | None = Field(
        default=None, description="The BGP configuration for anycast for a Grid member."
    )
    capture_traffic_control: dict[str, Any] | None = Field(default=None)
    capture_traffic_status: dict[str, Any] | None = Field(default=None)
    comment: str | None = Field(
        default=None, description="A descriptive comment of the Grid member."
    )
    config_addr_type: Literal["IPV4", "IPV6", "BOTH"] | str | None = Field(
        default=None, description="Address configuration type."
    )
    csp_access_key: list[str] | None = Field(
        default=None, description="CSP portal on-prem host access key"
    )
    csp_member_setting: dict[str, Any] | None = Field(default=None)
    dns_resolver_setting: dict[str, Any] | None = Field(
        default=None, description="DNS resolver settings used by the member."
    )
    dscp: int | None = Field(
        default=None, description="The DSCP (Differentiated Services Code Point) value."
    )
    email_setting: dict[str, Any] | None = Field(
        default=None, description="SMTP / email notification settings."
    )
    enable_ha: bool | None = Field(
        default=None, description="If set to True, the member has two physical nodes (HA pair)."
    )
    enable_lom: bool | None = Field(
        default=None, description="Determines if the LOM functionality is enabled or not."
    )
    enable_member_redirect: bool | None = Field(
        default=None,
        description="Determines if the member will redirect GUI connections to the Grid Master or not.",
    )
    enable_ro_api_access: bool | None = Field(
        default=None,
        description="If set to True and the member object is a Grid Master Candidate, then read-only API access is enabled.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    external_syslog_backup_servers: list[dict[str, Any]] | None = Field(
        default=None, description="The list of external syslog backup servers."
    )
    external_syslog_server_enable: bool | None = Field(
        default=None, description="Determines if external syslog servers should be enabled."
    )
    ha_cloud_platform: Literal["AWS", "AZURE", "GCP", "OCI"] | str | None = Field(
        default=None, description="Cloud platform for HA."
    )
    ha_on_cloud: bool | None = Field(
        default=None, description="True: HA on cloud. False: HA not on cloud."
    )
    host_name: str | None = Field(default=None, description="The host name of the Grid member.")
    ipv6_setting: dict[str, Any] | None = Field(default=None)
    ipv6_static_routes: list[dict[str, Any]] | None = Field(
        default=None, description="List of IPv6 static routes."
    )  # read-only
    is_dscp_capable: bool | None = Field(
        default=None,
        description="Determines if a Grid member supports DSCP (Differentiated Services Code Point).",
    )  # read-only
    is_master: bool | None = Field(
        default=None, description="Determines if a Grid member is a Grid Master or not."
    )
    lan2_enabled: bool | None = Field(
        default=None,
        description='If this is set to "true", the LAN2 port is enabled as an independent port or as a port for failover purposes.',
    )
    lan2_port_setting: dict[str, Any] | None = Field(default=None)
    lom_network_config: list[dict[str, Any]] | None = Field(
        default=None, description="The Network configurations for LOM."
    )
    lom_users: list[dict[str, Any]] | None = Field(
        default=None, description="The list of LOM users."
    )
    master_candidate: bool | None = Field(
        default=None,
        description="Determines if a Grid member is a Grid Master Candidate or not. This flag enables the Grid member to assume the role of the Grid Master as a disaster recovery measure.",
    )
    member_admin_operation: str | None = Field(default=None)
    member_service_communication: list[dict[str, Any]] | None = Field(
        default=None, description="Configure communication type for various services."
    )
    mgmt_port_setting: dict[str, Any] | None = Field(default=None)  # read-only
    mmdb_ea_build_time: int | None = Field(
        default=None, description="Extensible attributes Topology database build time."
    )  # read-only
    mmdb_geoip_build_time: int | None = Field(
        default=None, description="GeoIP Topology database build time."
    )
    nat_setting: dict[str, Any] | None = Field(default=None)
    node_info: list[dict[str, Any]] | None = Field(
        default=None,
        description="The node information list with detailed status report on the operations of the Grid Member, mgmt_port_setting must be enabled when configuring the MGMT Port using the node_info field.",
    )
    ntp_setting: dict[str, Any] | None = Field(
        default=None, description="NTP client/server settings."
    )
    ospf_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="The OSPF area configuration (for anycast) list for a Grid member.",
    )
    passive_ha_arp_enabled: bool | None = Field(
        default=None,
        description='The ARP protocol setting on the passive node of an HA pair. If you do not specify a value, the default value is "false". You can only set this value to "true" if the member is an HA pair.',
    )
    platform: Literal["INFOBLOX", "RIVERBED", "CISCO", "IBVM", "VNIOS"] | str | None = Field(
        default=None, description="Hardware Platform."
    )
    pre_provisioning: dict[str, Any] | None = Field(default=None)
    preserve_if_owns_delegation: bool | None = Field(
        default=None,
        description='Set this flag to "true" to prevent the deletion of the member if any delegated object remains attached to it.',
    )
    remote_console_access_enable: bool | None = Field(
        default=None,
        description="If set to True, superuser admins can access the Infoblox CLI from a remote location using an SSH (Secure Shell) v2 client.",
    )
    router_id: int | None = Field(
        default=None,
        description='Virtual router identifier. Provide this ID if "ha_enabled" is set to "true". This is a unique VRID number (from 1 to 255) for the local subnet.',
    )  # read-only
    service_status: list[dict[str, Any]] | None = Field(
        default=None, description="The service status list of a grid member."
    )
    service_type_configuration: Literal["ALL_V4", "ALL_V6", "CUSTOM"] | str | None = Field(
        default=None, description="Configure all services to the given type."
    )
    snmp_setting: dict[str, Any] | None = Field(default=None, description="SNMP agent settings.")
    static_routes: list[dict[str, Any]] | None = Field(
        default=None, description="List of static routes."
    )
    support_access_enable: bool | None = Field(
        default=None,
        description="Determines if support access for the Grid member should be enabled.",
    )  # read-only
    support_access_info: str | None = Field(
        default=None, description="The information string for support access."
    )
    syslog_proxy_setting: dict[str, Any] | None = Field(default=None)
    syslog_servers: list[dict[str, Any]] | None = Field(
        default=None, description="The list of external syslog servers."
    )
    syslog_size: int | None = Field(
        default=None, description="The maximum size for the syslog file expressed in megabytes."
    )
    threshold_traps: list[dict[str, Any]] | None = Field(
        default=None,
        description="Determines the list of threshold traps. The user can only change the values for each trap or remove traps.",
    )
    time_zone: str | None = Field(
        default=None,
        description='The time zone of the Grid member. The UTC string that represents the time zone, such as "Asia/Kolkata".',
    )
    traffic_capture_auth_dns_setting: dict[str, Any] | None = Field(
        default=None, description="Authoritative-DNS criteria for automated traffic capture."
    )
    traffic_capture_chr_setting: dict[str, Any] | None = Field(
        default=None, description="Cache-hit-ratio criteria for automated traffic capture."
    )
    traffic_capture_qps_setting: dict[str, Any] | None = Field(
        default=None, description="Queries-per-second criteria for automated traffic capture."
    )
    traffic_capture_rec_dns_setting: dict[str, Any] | None = Field(
        default=None, description="Recursive-DNS criteria for automated traffic capture."
    )
    traffic_capture_rec_queries_setting: dict[str, Any] | None = Field(
        default=None, description="Recursive-queries criteria for automated traffic capture."
    )
    trap_notifications: list[dict[str, Any]] | None = Field(
        default=None, description="Determines configuration of the trap notifications."
    )
    upgrade_group: str | None = Field(
        default=None,
        description="The name of the upgrade group to which this Grid member belongs.",
    )
    use_automated_traffic_capture: bool | None = Field(
        default=None,
        description="This flag is the use flag for enabling automated traffic capture based on DNS cache ratio thresholds.",
    )
    use_dns_resolver_setting: bool | None = Field(
        default=None, description="Use flag for: dns_resolver_setting"
    )
    use_dscp: bool | None = Field(default=None, description="Use flag for: dscp")
    use_email_setting: bool | None = Field(default=None, description="Use flag for: email_setting")
    use_enable_lom: bool | None = Field(default=None, description="Use flag for: enable_lom")
    use_enable_member_redirect: bool | None = Field(
        default=None, description="Use flag for: enable_member_redirect"
    )
    use_external_syslog_backup_servers: bool | None = Field(
        default=None, description="Use flag for: external_syslog_backup_servers"
    )
    use_remote_console_access_enable: bool | None = Field(
        default=None, description="Use flag for: remote_console_access_enable"
    )
    use_snmp_setting: bool | None = Field(default=None, description="Use flag for: snmp_setting")
    use_support_access_enable: bool | None = Field(
        default=None, description="Use flag for: support_access_enable"
    )
    use_syslog_proxy_setting: bool | None = Field(
        default=None,
        description="Use flag for: external_syslog_server_enable , syslog_servers, syslog_proxy_setting, syslog_size",
    )
    use_threshold_traps: bool | None = Field(
        default=None, description="Use flag for: threshold_traps"
    )
    use_time_zone: bool | None = Field(default=None, description="Use flag for: time_zone")
    use_traffic_capture_auth_dns: bool | None = Field(
        default=None,
        description="This flag is the use flag for enabling automated traffic capture based on authoritative DNS latency.",
    )
    use_traffic_capture_chr: bool | None = Field(
        default=None,
        description="This flag is the use flag for automated traffic capture settings at member level.",
    )
    use_traffic_capture_qps: bool | None = Field(
        default=None,
        description="This flag is the use flag for enabling automated traffic capture based on DNS queries per second thresholds.",
    )
    use_traffic_capture_rec_dns: bool | None = Field(
        default=None,
        description="This flag is the use flag for enabling automated traffic capture based on recursive DNS latency.",
    )
    use_traffic_capture_rec_queries: bool | None = Field(
        default=None,
        description="This flag is the use flag for enabling automated traffic capture based on outgoing recursive queries.",
    )
    use_trap_notifications: bool | None = Field(
        default=None, description="Use flag for: trap_notifications"
    )
    use_v4_vrrp: bool | None = Field(
        default=None, description='Specify "true" to use VRRPv4 or "false" to use VRRPv6.'
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    vip_setting: dict[str, Any] | None = Field(default=None)
    vpn_mtu: int | None = Field(
        default=None, description="The VPN maximum transmission unit (MTU)."
    )
    create_token: object | None = Field(
        default=None,
        description="Creates tokens for all available physical nodes on the member (virtual_node) and returns an array of records for pnode_token (physical_oid, token, and token_exp_date).",
    )
    read_token: object | None = Field(
        default=None,
        description="Returns tokens for all available physical nodes on the member (virtual_node).",
    )
    requestrestartservicestatus: object | None = Field(
        default=None,
        description="Use this function to request the Member service status. This function will refresh the restartservicestatus object.",
    )
    restartservices: object | None = Field(
        default=None, description="This function controls the Member services."
    )
