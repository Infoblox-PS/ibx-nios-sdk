# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordAaaa - NIOS DNS AAAA record.

All 25 properties from ``components.schemas.RecordAaaa`` in the v2.14 DNS
swagger are represented here.  Nested Record-AAAA-specific types are defined
inline; ``CloudInfo`` is reused from ``_shared.py``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.dns.models._shared import CloudInfo, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "aws_rte53_record_info",
        "cloud_info",
        "creation_time",
        "discovered_data",
        "dns_name",
        "last_queried",
        "ms_ad_user_data",
        "reclaimable",
        "shared_record_group",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# RecordAaaa-specific nested types (inline, not shared)
# ---------------------------------------------------------------------------


class RecordAaaaDiscoveredData(_DnsNested):
    """Discovery metadata attached to an AAAA record (read-only props).

    All fields are read-only as populated by NIOS device discovery.
    """

    device_model: str | None = Field(
        default=None, description="The model name of the end device in the vendor terminology."
    )
    device_port_name: str | None = Field(
        default=None,
        description="The system name of the interface associated with the discovered IP address.",
    )
    device_port_type: str | None = Field(
        default=None,
        description="The hardware type of the interface associated with the discovered IP address.",
    )
    device_type: str | None = Field(
        default=None, description="The type of end host in vendor terminology."
    )
    device_vendor: str | None = Field(default=None, description="The vendor name of the end host.")
    discovered_name: str | None = Field(
        default=None,
        description="The name of the network device associated with the discovered IP address.",
    )
    discoverer: str | None = Field(
        default=None,
        description="Specifies whether the IP address was discovered by a NetMRI or NIOS discovery process.",
    )
    duid: str | None = Field(
        default=None,
        description="For IPv6 address only. The DHCP unique identifier of the discovered host. This is an optional field, and data might not be included.",
    )
    first_discovered: int | None = Field(
        default=None,
        description="The date and time the IP address was first discovered in Epoch seconds format.",
    )
    iprg_no: int | None = Field(default=None, description="The port redundant group number.")
    iprg_state: Literal["VIP", "ACTIVE", "STANDBY", "NEGOTIATION"] | str | None = Field(
        default=None, description="The status for the IP address within port redundant group."
    )
    iprg_type: Literal["HSRP", "VRRP"] | str | None = Field(
        default=None, description="The port redundant group type."
    )
    last_discovered: int | None = Field(
        default=None,
        description="The date and time the IP address was last discovered in Epoch seconds format.",
    )
    mac_address: str | None = Field(
        default=None,
        description="The discovered MAC address for the host. This is the unique identifier of a network device. The discovery acquires the MAC address for hosts that are located on the same network as the Grid member that is running the discovery. This can also be the MAC address of a virtual entity on a specified vSphere server.",
    )
    mgmt_ip_address: str | None = Field(
        default=None,
        description="The management IP address of the end host that has more than one IP.",
    )
    netbios_name: str | None = Field(
        default=None,
        description="The name returned in the NetBIOS reply or the name you manually register for the discovered host.",
    )
    network_component_description: str | None = Field(
        default=None,
        description="A textual description of the switch that is connected to the end device.",
    )
    network_component_ip: str | None = Field(
        default=None,
        description="The IPv4 Address or IPv6 Address of the switch that is connected to the end device.",
    )
    network_component_model: str | None = Field(
        default=None,
        description="Model name of the switch port connected to the end host in vendor terminology.",
    )
    network_component_name: str | None = Field(
        default=None,
        description="If a reverse lookup was successful for the IP address associated with this switch, the host name is displayed in this field.",
    )
    network_component_port_description: str | None = Field(
        default=None,
        description="A textual description of the switch port that is connected to the end device.",
    )
    network_component_port_name: str | None = Field(
        default=None, description="The name of the switch port connected to the end device."
    )
    network_component_port_number: str | None = Field(
        default=None, description="The number of the switch port connected to the end device."
    )
    network_component_type: str | None = Field(
        default=None, description="Identifies the switch that is connected to the end device."
    )
    network_component_vendor: str | None = Field(
        default=None, description="The vendor name of the switch port connected to the end host."
    )
    open_ports: str | None = Field(
        default=None,
        description='The list of opened ports on the IP address, represented as: "TCP: 21,22,23 UDP: 137,139". Limited to max total 1000 ports.',
    )
    os: str | None = Field(
        default=None,
        description="The operating system of the detected host or virtual entity. The OS can be one of the following: * Microsoft for all discovered hosts that have a non-null value in the MAC addresses using the NetBIOS discovery method. * A value that a TCP discovery returns. * The OS of a virtual entity on a vSphere server.",
    )
    port_duplex: str | None = Field(
        default=None,
        description="The negotiated or operational duplex setting of the switch port connected to the end device.",
    )
    port_link_status: str | None = Field(
        default=None,
        description="The link status of the switch port connected to the end device. Indicates whether it is connected.",
    )
    port_speed: str | None = Field(
        default=None, description="The interface speed, in Mbps, of the switch port."
    )
    port_status: str | None = Field(
        default=None,
        description="The operational status of the switch port. Indicates whether the port is up or down.",
    )
    port_type: str | None = Field(default=None, description="The type of switch port.")
    port_vlan_description: str | None = Field(
        default=None,
        description="The description of the VLAN of the switch port that is connected to the end device.",
    )
    port_vlan_name: str | None = Field(
        default=None, description="The name of the VLAN of the switch port."
    )
    port_vlan_number: str | None = Field(
        default=None, description="The ID of the VLAN of the switch port."
    )
    v_adapter: str | None = Field(
        default=None,
        description="The name of the physical network adapter through which the virtual entity is connected to the appliance.",
    )
    v_cluster: str | None = Field(
        default=None,
        description="The name of the VMware cluster to which the virtual entity belongs.",
    )
    v_datacenter: str | None = Field(
        default=None,
        description="The name of the vSphere datacenter or container to which the virtual entity belongs.",
    )
    v_entity_name: str | None = Field(default=None, description="The name of the virtual entity.")
    v_entity_type: str | None = Field(
        default=None,
        description="The virtual entity type. This can be blank or one of the following: Virtual Machine, Virtual Host, or Virtual Center. Virtual Center represents a VMware vCenter server.",
    )
    v_host: str | None = Field(
        default=None,
        description="The name of the VMware server on which the virtual entity was discovered.",
    )
    v_switch: str | None = Field(
        default=None,
        description="The name of the switch to which the virtual entity is connected.",
    )
    vmi_name: str | None = Field(default=None, description="Name of the virtual machine.")
    vmi_id: str | None = Field(default=None, description="ID of the virtual machine.")
    vlan_port_group: str | None = Field(
        default=None, description="Port group which the virtual machine belongs to."
    )
    vswitch_name: str | None = Field(default=None, description="Name of the virtual switch.")
    vswitch_id: str | None = Field(default=None, description="ID of the virtual switch.")
    vswitch_type: Literal["Unknown", "Standard", "Distributed"] | str | None = Field(
        default=None, description="Type of the virtual switch: standard or distributed."
    )
    vswitch_ipv6_enabled: bool | None = Field(
        default=None, description="Indicates the virtual switch has IPV6 enabled."
    )
    vport_name: str | None = Field(
        default=None,
        description="Name of the network adapter on the virtual switch connected with the virtual machine.",
    )
    vport_mac_address: str | None = Field(
        default=None,
        description="MAC address of the network adapter on the virtual switch where the virtual machine connected to.",
    )
    vport_link_status: str | None = Field(
        default=None,
        description="Link status of the network adapter on the virtual switch where the virtual machine connected to.",
    )
    vport_conf_speed: str | None = Field(
        default=None,
        description="Configured speed of the network adapter on the virtual switch where the virtual machine connected to. Unit is kb.",
    )
    vport_conf_mode: Literal["Unknown", "Full-duplex", "Half-duplex"] | str | None = Field(
        default=None,
        description="Configured mode of the network adapter on the virtual switch where the virtual machine connected to.",
    )
    vport_speed: str | None = Field(
        default=None,
        description="Actual speed of the network adapter on the virtual switch where the virtual machine connected to. Unit is kb.",
    )
    vport_mode: Literal["Unknown", "Full-duplex", "Half-duplex"] | str | None = Field(
        default=None,
        description="Actual mode of the network adapter on the virtual switch where the virtual machine connected to.",
    )
    vswitch_segment_type: str | None = Field(
        default=None,
        description="Type of the network segment on which the current virtual machine/vport connected to.",
    )
    vswitch_segment_name: str | None = Field(
        default=None,
        description="Name of the network segment on which the current virtual machine/vport connected to.",
    )
    vswitch_segment_id: str | None = Field(
        default=None,
        description="ID of the network segment on which the current virtual machine/vport connected to.",
    )
    vswitch_segment_port_group: str | None = Field(
        default=None,
        description="Port group of the network segment on which the current virtual machine/vport connected to.",
    )
    vswitch_available_ports_count: int | None = Field(
        default=None,
        description="Numer of available ports reported by the virtual switch on which the virtual machine/vport connected to.",
    )
    vswitch_tep_type: str | None = Field(
        default=None, description="Type of virtual tunnel endpoint (VTEP) in the virtual switch."
    )
    vswitch_tep_ip: str | None = Field(
        default=None,
        description="IP address of the virtual tunnel endpoint (VTEP) in the virtual switch.",
    )
    vswitch_tep_port_group: str | None = Field(
        default=None,
        description="Port group of the virtual tunnel endpoint (VTEP) in the virtual switch.",
    )
    vswitch_tep_vlan: str | None = Field(
        default=None,
        description="VLAN of the virtual tunnel endpoint (VTEP) in the virtual switch.",
    )
    vswitch_tep_dhcp_server: str | None = Field(
        default=None,
        description="DHCP server of the virtual tunnel endpoint (VTEP) in the virtual switch.",
    )
    vswitch_tep_multicast: str | None = Field(
        default=None,
        description="Muticast address of the virtual tunnel endpoint (VTEP) in the virtual swtich.",
    )
    vmhost_ip_address: str | None = Field(
        default=None,
        description="IP address of the physical node on which the virtual machine is hosted.",
    )
    vmhost_name: str | None = Field(
        default=None,
        description="Name of the physical node on which the virtual machine is hosted.",
    )
    vmhost_mac_address: str | None = Field(
        default=None,
        description="MAC address of the physical node on which the virtual machine is hosted.",
    )
    vmhost_subnet_cidr: int | None = Field(
        default=None,
        description="CIDR subnet of the physical node on which the virtual machine is hosted.",
    )
    vmhost_nic_names: str | None = Field(
        default=None,
        description='List of all physical port names used by the virtual switch on the physical node on which the virtual machine is hosted. Represented as: "eth1,eth2,eth3".',
    )
    vmi_tenant_id: str | None = Field(
        default=None, description="ID of the tenant which virtual machine belongs to."
    )
    cmp_type: str | None = Field(
        default=None,
        description="If the IP is coming from a Cloud environment, the Cloud Management Platform type.",
    )
    vmi_ip_type: str | None = Field(default=None, description="Discovered IP address type.")
    vmi_private_address: str | None = Field(
        default=None, description="Private IP address of the virtual machine."
    )
    vmi_is_public_address: bool | None = Field(
        default=None, description="Indicates whether the IP address is a public address."
    )
    cisco_ise_ssid: str | None = Field(default=None, description="The Cisco ISE SSID.")
    cisco_ise_endpoint_profile: str | None = Field(
        default=None, description="The Endpoint Profile created in Cisco ISE."
    )
    cisco_ise_session_state: (
        Literal["AUTHENTICATED", "AUTHENTICATING", "DISCONNECTED", "POSTURED", "STARTED"]
        | str
        | None
    ) = Field(default=None, description="The Cisco ISE connection session state.")
    cisco_ise_security_group: str | None = Field(
        default=None, description="The Cisco ISE security group name."
    )
    task_name: str | None = Field(default=None, description="The name of the discovery task.")
    network_component_location: str | None = Field(
        default=None,
        description="Location of the network component on which the IP address was discovered.",
    )
    network_component_contact: str | None = Field(
        default=None,
        description="Contact information from the network component on which the IP address was discovered.",
    )
    device_location: str | None = Field(
        default=None, description="Location of device on which the IP address was discovered."
    )
    device_contact: str | None = Field(
        default=None,
        description="Contact information from device on which the IP address was discovered.",
    )
    ap_name: str | None = Field(
        default=None, description="Discovered name of Wireless Access Point."
    )
    ap_ip_address: str | None = Field(
        default=None, description="Discovered IP address of Wireless Access Point."
    )
    ap_ssid: str | None = Field(
        default=None,
        description="Service set identifier (SSID) associated with Wireless Access Point.",
    )
    bridge_domain: str | None = Field(default=None, description="Discovered bridge domain.")
    endpoint_groups: str | None = Field(
        default=None, description="A comma-separated list of the discovered endpoint groups."
    )
    tenant: str | None = Field(default=None, description="Discovered tenant.")
    vrf_name: str | None = Field(default=None, description="The name of the VRF.")
    vrf_description: str | None = Field(default=None, description="Description of the VRF.")
    vrf_rd: str | None = Field(default=None, description="Route distinguisher of the VRF.")
    bgp_as: int | None = Field(default=None, description="The BGP autonomous system number.")


class RecordAaaaMsAdUserData(_DnsNested):
    """Microsoft Active Directory user data for an AAAA record."""

    active_users_count: int | None = Field(default=None, description="The number of active users.")


class RecordAaaaAwsRte53RecordInfo(_DnsNested):
    """AWS Route 53 record metadata attached to an AAAA record."""

    alias_target_dns_name: str | None = Field(
        default=None, description="DNS name of the alias target."
    )
    alias_target_hosted_zone_id: str | None = Field(
        default=None, description="Hosted zone ID of the alias target."
    )
    alias_target_evaluate_target_health: bool | None = Field(
        default=None,
        description="Indicates if Amazon Route 53 evaluates the health of the alias target.",
    )
    failover: Literal["PRIMARY", "SECONDARY"] | str | None = Field(
        default=None,
        description="Indicates whether this is the primary or secondary resource record for Amazon Route 53 failover routing.",
    )
    geolocation_continent_code: str | None = Field(
        default=None, description="Continent code for Amazon Route 53 geolocation routing."
    )
    geolocation_country_code: str | None = Field(
        default=None, description="Country code for Amazon Route 53 geolocation routing."
    )
    geolocation_subdivision_code: str | None = Field(
        default=None, description="Subdivision code for Amazon Route 53 geolocation routing."
    )
    health_check_id: str | None = Field(
        default=None,
        description="ID of the health check that Amazon Route 53 performs for this resource record.",
    )
    region: str | None = Field(
        default=None,
        description="Amazon EC2 region where this resource record resides for latency routing.",
    )
    set_identifier: str | None = Field(
        default=None,
        description="An identifier that differentiates records with the same DNS name and type for weighted, latency, geolocation, and failover routing.",
    )
    type: (
        Literal["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SPF", "SRV", "TXT"] | str | None
    ) = Field(default=None, description="Type of Amazon Route 53 resource record.")
    weight: int | None = Field(
        default=None,
        description="Value that determines the portion of traffic for this record in weighted routing. The range is from 0 to 255.",
    )  # ---------------------------------------------------------------------------


# Main RecordAaaa model
# ---------------------------------------------------------------------------


class RecordAaaa(BaseModel):
    """NIOS DNS AAAA record.

    All 25 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- AWS Route 53 info (read-only in practice) ---
    aws_rte53_record_info: RecordAaaaAwsRte53RecordInfo | None = Field(
        default=None, description="AWS Route53 record info populated by Route53 sync."
    )  # --- cloud info (reused shared type) ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common fields ---
    comment: str | None = Field(
        default=None, description="Comment for the record; maximum 256 characters."
    )  # --- read-only ---
    creation_time: int | None = Field(
        default=None, description="The time of the record creation in Epoch seconds format."
    )  # --- DDNS ---
    creator: Literal["STATIC", "DYNAMIC", "SYSTEM"] | str | None = Field(
        default=None,
        description="The record creator. Note that changing creator from or to 'SYSTEM' value is not allowed.",
    )
    ddns_principal: str | None = Field(
        default=None, description="The GSS-TSIG principal that owns this record."
    )
    ddns_protected: bool | None = Field(
        default=None,
        description="Determines if the DDNS updates for this record are allowed or not.",
    )  # --- record state ---
    disable: bool | None = Field(
        default=None,
        description="Determines if the record is disabled or not. False means that the record is enabled.",
    )  # --- discovery ---
    discovered_data: RecordAaaaDiscoveredData | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )  # --- read-only ---
    dns_name: str | None = Field(
        default=None, description="The name for an AAAA record in punycode format."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- reclamation ---
    forbid_reclamation: bool | None = Field(
        default=None, description="Determines if the reclamation is allowed for the record or not."
    )  # --- core identity ---
    ipv6addr: str | None = Field(
        default=None, description="The IPv6 Address of the record."
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- MS AD user data ---
    ms_ad_user_data: RecordAaaaMsAdUserData | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="Name for the AAAA record in FQDN format. This value can be in unicode format.",
    )  # --- read-only ---
    reclaimable: bool | None = Field(
        default=None, description="Determines if the record is reclaimable or not."
    )  # --- PTR management ---
    remove_associated_ptr: bool | None = Field(
        default=None,
        description="Delete option that indicates whether the associated PTR records should be removed while deleting the specified A record.",
    )  # --- read-only ---
    shared_record_group: str | None = Field(
        default=None,
        description="The name of the shared record group in which the record resides. This field exists only on db_objects if this record is a shared record.",
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for the record. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
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
