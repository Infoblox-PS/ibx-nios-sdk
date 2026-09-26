# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiVmaddress - NIOS Grid Cloud API VM address (mostly read-only)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "address_type",
        "associated_ip",
        "associated_object_types",
        "associated_objects",
        "cloud_info",
        "dns_names",
        "elastic_address",
        "interface_name",
        "is_ipv4",
        "mac_address",
        "ms_ad_user_data",
        "network",
        "network_view",
        "port_id",
        "private_address",
        "private_hostname",
        "public_address",
        "public_hostname",
        "subnet_address",
        "subnet_cidr",
        "subnet_id",
        "tenant",
        "vm_availability_zone",
        "vm_comment",
        "vm_creation_time",
        "vm_hostname",
        "vm_id",
        "vm_kernel_id",
        "vm_last_update_time",
        "vm_name",
        "vm_network_count",
        "vm_operating_system",
        "vm_type",
        "vm_vpc_address",
        "vm_vpc_cidr",
        "vm_vpc_id",
        "vm_vpc_name",
        "vm_vpc_ref",
    }
)


class GridCloudapiVmaddress(BaseModel):
    """NIOS Grid Cloud API VM address."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    address: str | None = Field(default=None, description="The IP address of the interface.")
    address_type: str | None = Field(
        default=None, description="IP address type (Public, Private, Elastic, Floating, ...)."
    )
    associated_ip: str | None = Field(
        default=None, description="Reference to associated IPv4 or IPv6 address."
    )
    associated_object_types: list[str] | None = Field(
        default=None,
        description='Array of string denoting the types of underlying objects IPv4/IPv6 - "A", "AAAA", "PTR", "HOST", "FA", "RESERVATION", "UNMANAGED" + ("BULKHOST", "DHCP_RANGE", "RESERVED_RANGE", "LEASE", "NETWORK", "BROADCAST", "PENDING"),',
    )
    associated_objects: list[str] | None = Field(
        default=None,
        description="The list of references to the object (Host, Fixed Address, RR, ...) that defines this IP.",
    )
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # read-only
    dns_names: list[str] | None = Field(
        default=None, description="The list of all FQDNs associated with the IP address."
    )
    elastic_address: str | None = Field(
        default=None,
        description="Elastic IP address associated with this private address, if this address is a private address; otherwise empty.",
    )
    interface_name: str | None = Field(
        default=None, description="Name of the interface associated with this IP address."
    )
    is_ipv4: bool | None = Field(
        default=None, description="Indicates whether the address is IPv4 or IPv6."
    )
    mac_address: str | None = Field(default=None, description="The MAC address of the interface.")
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # read-only
    network: str | None = Field(
        default=None,
        description="The network to which this address belongs, in IPv4 Address/CIDR format.",
    )
    network_view: str | None = Field(
        default=None, description="Network view name of the delegated object."
    )
    port_id: int | None = Field(default=None, description="Port identifier of the interface.")
    private_address: str | None = Field(
        default=None,
        description="Private IP address associated with this public (or elastic or floating) address, if this address is a public address; otherwise empty.",
    )
    private_hostname: str | None = Field(
        default=None,
        description="Host part of the FQDN of this address if this address is a private address; otherwise empty",
    )
    public_address: str | None = Field(
        default=None,
        description="Public IP address associated with this private address, if this address is a private address; otherwise empty.",
    )
    public_hostname: str | None = Field(
        default=None,
        description="Host part of the FQDN of this address if this address is a public (or elastic or floating) address; otherwise empty",
    )
    subnet_address: str | None = Field(
        default=None,
        description="Network address of the subnet that is the container of this address.",
    )
    subnet_cidr: int | None = Field(
        default=None, description="CIDR of the subnet that is the container of this address."
    )
    subnet_id: str | None = Field(
        default=None, description="Subnet ID that is the container of this address."
    )
    tenant: str | None = Field(default=None, description="The Cloud API Tenant object.")
    vm_availability_zone: str | None = Field(
        default=None, description="Availability zone of the VM."
    )
    vm_comment: str | None = Field(default=None, description="VM comment.")
    vm_creation_time: int | None = Field(
        default=None, description="Date/time the VM was first created as NIOS object."
    )
    vm_hostname: str | None = Field(
        default=None,
        description="Host part of the FQDN of the address attached to the primary interface.",
    )
    vm_id: str | None = Field(default=None, description="The UUID of the Virtual Machine.")
    vm_kernel_id: str | None = Field(
        default=None, description="Kernel ID of the VM that this address is associated with."
    )
    vm_last_update_time: int | None = Field(
        default=None, description="Last time the VM was updated."
    )
    vm_name: str | None = Field(default=None, description="The name of the Virtual Machine.")
    vm_network_count: int | None = Field(
        default=None, description="Count of networks containing all the addresses of the VM."
    )
    vm_operating_system: str | None = Field(
        default=None, description="Operating system that the VM is running."
    )
    vm_type: str | None = Field(
        default=None, description="Type of the VM this address is associated with."
    )
    vm_vpc_address: str | None = Field(
        default=None,
        description="Network address of the VPC of the VM that this address is associated with.",
    )
    vm_vpc_cidr: int | None = Field(
        default=None, description="CIDR of the VPC of the VM that this address is associated with."
    )
    vm_vpc_id: str | None = Field(
        default=None, description="Identifier of the VPC where the VM is defined."
    )
    vm_vpc_name: str | None = Field(
        default=None, description="Name of the VPC where the VM is defined."
    )
    vm_vpc_ref: str | None = Field(
        default=None, description="Reference to the VPC where the VM is defined."
    )
