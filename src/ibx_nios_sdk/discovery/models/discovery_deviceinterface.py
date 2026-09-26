# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceinterface - NIOS discovered device interface.

Operations: GET (collection and by ref), PUT (limited fields: description,
admin_status, vlan_info_task_info).

NOTE: ``type`` is a Python keyword collision - aliased as ``type_``.
Nested objects represented as ``dict[str, Any] | None``.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "admin_status",
        "admin_status_task_info",
        "aggr_interface_name",
        "cap_if_admin_status_ind",
        "cap_if_admin_status_na_reason",
        "cap_if_description_ind",
        "cap_if_description_na_reason",
        "cap_if_net_deprovisioning_ipv4_ind",
        "cap_if_net_deprovisioning_ipv4_na_reason",
        "cap_if_net_deprovisioning_ipv6_ind",
        "cap_if_net_deprovisioning_ipv6_na_reason",
        "cap_if_net_provisioning_ipv4_ind",
        "cap_if_net_provisioning_ipv4_na_reason",
        "cap_if_net_provisioning_ipv6_ind",
        "cap_if_net_provisioning_ipv6_na_reason",
        "cap_if_vlan_assignment_ind",
        "cap_if_vlan_assignment_na_reason",
        "cap_if_voice_vlan_ind",
        "cap_if_voice_vlan_na_reason",
        "description",
        "description_task_info",
        "device",
        "duplex",
        "ifaddr_infos",
        "index",
        "last_change",
        "link_aggregation",
        "mac",
        "ms_ad_user_data",
        "name",
        "network_view",
        "oper_status",
        "port_fast",
        "reserved_object",
        "speed",
        "trunk_status",
        "type",
        "type_",
        "vlan_info_task_info",
        "vlan_infos",
        "vpc_peer",
        "vpc_peer_device",
        "vrf_description",
        "vrf_name",
        "vrf_rd",
    }
)


class DiscoveryDeviceinterface(BaseModel):
    """NIOS discovered device interface."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    aggr_interface_name: str | None = Field(
        default=None, description="Name of the port channel current interface belongs to."
    )
    cap_if_admin_status_ind: bool | None = Field(
        default=None, description="Determines whether to modify the admin status of the interface."
    )
    cap_if_admin_status_na_reason: str | None = Field(
        default=None, description="The reason that the edit admin status action is not available."
    )
    cap_if_description_ind: bool | None = Field(
        default=None, description="Determines whether to modify the description of the interface."
    )
    cap_if_description_na_reason: str | None = Field(
        default=None, description="The reason that the edit description action is not available."
    )
    cap_if_net_deprovisioning_ipv4_ind: bool | None = Field(
        default=None,
        description="Determines whether to deprovision a IPv4 network from the interfaces.",
    )
    cap_if_net_deprovisioning_ipv4_na_reason: str | None = Field(
        default=None,
        description="The reason that the deprovision a IPv4 network from the interface.",
    )
    cap_if_net_deprovisioning_ipv6_ind: bool | None = Field(
        default=None,
        description="Determines whether to deprovision a IPv6 network from the interfaces.",
    )
    cap_if_net_deprovisioning_ipv6_na_reason: str | None = Field(
        default=None,
        description="The reason that the deprovision a IPv6 network from the interface.",
    )
    cap_if_net_provisioning_ipv4_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the IPv4 network associated to the interface.",
    )
    cap_if_net_provisioning_ipv4_na_reason: str | None = Field(
        default=None, description="The reason that IPv4 network provisioning is not available."
    )
    cap_if_net_provisioning_ipv6_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the IPv6 network associated to the interface.",
    )
    cap_if_net_provisioning_ipv6_na_reason: str | None = Field(
        default=None, description="The reason that IPv6 network provisioning is not available."
    )
    cap_if_vlan_assignment_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the VLAN assignment of the interface.",
    )
    cap_if_vlan_assignment_na_reason: str | None = Field(
        default=None, description="The reason that VLAN assignment action is not available."
    )
    cap_if_voice_vlan_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the voice VLAN assignment of the interface.",
    )
    cap_if_voice_vlan_na_reason: str | None = Field(
        default=None, description="The reason that voice VLAN assignment action is not available."
    )
    device: str | None = Field(
        default=None, description="The ref to the device to which the interface belongs."
    )
    duplex: Literal["FULL", "HALF", "UNSUPPORTED", "UNKNOWN"] | str | None = Field(
        default=None, description="The duplex state of the interface."
    )
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    ifaddr_infos: list[dict[str, Any]] | None = Field(
        default=None, description="List of IFaddr information associated with the interface."
    )
    index: int | None = Field(
        default=None, description="The interface index number, as reported by SNMP."
    )
    last_change: int | None = Field(
        default=None, description="Timestamp of the last interface property change detected."
    )
    link_aggregation: bool | None = Field(
        default=None, description="This field indicates if this is a link aggregation interface."
    )
    mac: str | None = Field(default=None, description="The MAC address of the interface.")
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )
    name: str | None = Field(default=None, description="The interface system name.")
    network_view: str | None = Field(default=None, description="Th name of the network view.")
    oper_status: Literal["UP", "DOWN"] | str | None = Field(
        default=None, description="Operating state of the interface."
    )
    port_fast: Literal["ENABLED", "DISABLED"] | str | None = Field(
        default=None, description="The Port Fast status of the interface."
    )
    reserved_object: str | None = Field(
        default=None,
        description="The reference to object(Host/FixedAddress/GridMember) to which this port is reserved.",
    )
    speed: int | None = Field(default=None, description="The interface speed in bps.")
    trunk_status: Literal["ON", "OFF"] | str | None = Field(
        default=None, description="Indicates if the interface is tagged as a VLAN trunk or not."
    )
    vlan_infos: list[dict[str, Any]] | None = Field(
        default=None, description="The list of VLAN information associated with the interface."
    )
    vpc_peer: str | None = Field(
        default=None,
        description="Aggregated interface name of vPC peer device current port is connected to.",
    )
    vpc_peer_device: str | None = Field(
        default=None, description="The reference to vPC peer device."
    )
    vrf_description: str | None = Field(
        default=None,
        description="The description of the Virtual Routing and Forwarding (VRF) associated with the interface.",
    )
    vrf_name: str | None = Field(
        default=None,
        description="The name of the Virtual Routing and Forwarding (VRF) associated with the interface.",
    )
    vrf_rd: str | None = Field(
        default=None,
        description="The route distinguisher of the Virtual Routing and Forwarding (VRF) associated with the interface.",
    )  # Python keyword collision: type → type_
    type_: str | None = Field(default=None, alias="type", description="Object type discriminator.")

    # --- writable ---
    admin_status: Literal["UP", "DOWN"] | str | None = Field(
        default=None, description="Administrative state of the interface."
    )
    admin_status_task_info: dict[str, Any] | None = Field(default=None)
    description: str | None = Field(default=None, description="The description of the interface.")
    description_task_info: dict[str, Any] | None = Field(default=None)
    vlan_info_task_info: dict[str, Any] | None = Field(default=None)
