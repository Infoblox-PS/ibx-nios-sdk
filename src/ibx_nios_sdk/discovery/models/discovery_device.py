# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDevice - NIOS discovered network device (read-only aggregate).

Operations: GET (collection and by ref), PUT (limited writable fields).

NOTE: ``type`` is a Python keyword collision - aliased as ``type_``.
Nested objects (ms_ad_user_data, port_stats, network_infos, vlan_infos,
interfaces, neighbors) are deeply nested → ``dict[str, Any] | None``.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# Swagger marks no fields as x-readonly, but device is a read-mostly aggregate.
# The only writable fields per WAPI are: name, user_defined_mgmt_ip, privileged_polling.
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "address_ref",
        "available_mgmt_ips",
        "cap_admin_status_ind",
        "cap_admin_status_na_reason",
        "cap_description_ind",
        "cap_description_na_reason",
        "cap_net_deprovisioning_ind",
        "cap_net_deprovisioning_na_reason",
        "cap_net_provisioning_ind",
        "cap_net_provisioning_na_reason",
        "cap_net_vlan_provisioning_ind",
        "cap_net_vlan_provisioning_na_reason",
        "cap_vlan_assignment_ind",
        "cap_vlan_assignment_na_reason",
        "cap_voice_vlan_ind",
        "cap_voice_vlan_na_reason",
        "chassis_serial_number",
        "description",
        "interfaces",
        "location",
        "model",
        "ms_ad_user_data",
        "name",
        "neighbors",
        "network",
        "network_infos",
        "network_view",
        "networks",
        "os_version",
        "port_stats",
        "type",
        "type_",
        "vendor",
        "vlan_infos",
    }
)


class DiscoveryDevice(BaseModel):
    """NIOS discovered network device - read-mostly aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only / aggregate ---
    address: str | None = Field(
        default=None, description="The IPv4 Address or IPv6 Address of the device."
    )
    address_ref: str | None = Field(
        default=None, description="The ref to management IP address of the device."
    )
    available_mgmt_ips: list[str] | None = Field(
        default=None, description="The list of available management IPs for the device."
    )
    cap_admin_status_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the admin status of an interface of the device.",
    )
    cap_admin_status_na_reason: str | None = Field(
        default=None, description="The reason that the edit admin status action is not available."
    )
    cap_description_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the description of an interface on the device.",
    )
    cap_description_na_reason: str | None = Field(
        default=None, description="The reason that the edit description action is not available."
    )
    cap_net_deprovisioning_ind: bool | None = Field(
        default=None,
        description="Determines whether to deprovision a network from interfaces of the device.",
    )
    cap_net_deprovisioning_na_reason: str | None = Field(
        default=None,
        description="The reason that the deprovision a network from interfaces of this device is not available.",
    )
    cap_net_provisioning_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the network associated to an interface of the device.",
    )
    cap_net_provisioning_na_reason: str | None = Field(
        default=None, description="The reason that network provisioning is not available."
    )
    cap_net_vlan_provisioning_ind: bool | None = Field(
        default=None,
        description="Determines whether to create a VLAN and then provision a network to the interface of the device.",
    )
    cap_net_vlan_provisioning_na_reason: str | None = Field(
        default=None, description="The reason that network provisioning on VLAN is not available."
    )
    cap_vlan_assignment_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the VLAN assignment of an interface of the device.",
    )
    cap_vlan_assignment_na_reason: str | None = Field(
        default=None, description="The reason that VLAN assignment action is not available."
    )
    cap_voice_vlan_ind: bool | None = Field(
        default=None,
        description="Determines whether to modify the voice VLAN assignment of an interface of the device.",
    )
    cap_voice_vlan_na_reason: str | None = Field(
        default=None, description="The reason that voice VLAN assignment action is not available."
    )
    chassis_serial_number: str | None = Field(
        default=None, description="The device chassis serial number."
    )
    description: str | None = Field(default=None, description="The description of the device.")
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    interfaces: list[dict[str, Any]] | None = Field(
        default=None, description="List of the device interfaces."
    )
    location: str | None = Field(default=None, description="The location of the device.")
    model: str | None = Field(default=None, description="The model name of the device.")
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )
    neighbors: list[dict[str, Any]] | None = Field(
        default=None, description="List of the device neighbors."
    )
    network: str | None = Field(
        default=None,
        description="The ref to the network to which belongs the management IP address belongs.",
    )
    network_infos: list[dict[str, Any]] | None = Field(
        default=None, description="The list of networks to which the device interfaces belong."
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this device resides."
    )
    networks: list[str] | None = Field(
        default=None, description="The list of networks to which the device interfaces belong."
    )
    os_version: str | None = Field(
        default=None, description="The Operating System version running on the device."
    )
    port_stats: dict[str, Any] | None = Field(default=None)
    vlan_infos: list[dict[str, Any]] | None = Field(
        default=None, description="The list of VLAN information associated with the device."
    )
    vendor: str | None = Field(
        default=None, description="The vendor name of the device."
    )  # Python keyword collision: type → type_
    type_: str | None = Field(default=None, alias="type", description="Object type discriminator.")

    # --- writable ---
    name: str | None = Field(default=None, description="The name of the device.")
    privileged_polling: bool | None = Field(
        default=None,
        description="A flag indicated that NI should send enable command when interacting with device.",
    )
    user_defined_mgmt_ip: str | None = Field(
        default=None, description="User-defined management IP address of the device."
    )
