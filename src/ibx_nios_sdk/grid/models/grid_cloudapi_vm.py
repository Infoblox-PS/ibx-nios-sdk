# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiVm - NIOS Grid Cloud API VM."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "availability_zone",
        "cloud_info",
        "elastic_ip_address",
        "first_seen",
        "hostname",
        "id",
        "last_seen",
        "network_count",
        "primary_mac_address",
        "subnet_address",
        "subnet_cidr",
        "subnet_id",
        "tenant_name",
        "uuid",
        "vpc_address",
        "vpc_cidr",
        "vpc_id",
        "vpc_name",
    }
)


class GridCloudapiVm(BaseModel):
    """NIOS Grid Cloud API VM."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    availability_zone: str | None = Field(default=None, description="Availability zone of the VM.")
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )
    comment: str | None = Field(
        default=None, description="Comment for the vm object; maximum 1024 characters."
    )  # read-only
    elastic_ip_address: str | None = Field(
        default=None, description="Elastic IP address associated with the VM's primary interface."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # read-only
    first_seen: int | None = Field(
        default=None, description="The timestamp when the VM was first seen in the system."
    )  # read-only
    hostname: str | None = Field(
        default=None,
        description="Hostname part of the FQDN for the address associated with the VM's primary interface.",
    )  # read-only
    id: str | None = Field(
        default=None,
        description="Unique ID associated with the VM. This is set only when the VM is first created.",
    )
    kernel_id: str | None = Field(
        default=None,
        description="Identifier of the kernel that this VM is running; maximum 128 characters.",
    )  # read-only
    last_seen: int | None = Field(
        default=None,
        description="The timestamp when the last event associated with the VM happened.",
    )
    name: str | None = Field(default=None, description="Name of the VM.")  # read-only
    network_count: int | None = Field(
        default=None,
        description="Number of Networks containing any address associated with this VM.",
    )
    operating_system: str | None = Field(
        default=None,
        description="Guest Operating system that this VM is running; maximum 128 characters.",
    )  # read-only
    primary_mac_address: str | None = Field(
        default=None, description="MAC address associated with the VM's primary interface."
    )  # read-only
    subnet_address: str | None = Field(
        default=None,
        description="Address of the network that is the container of the address associated with the VM's primary interface.",
    )  # read-only
    subnet_cidr: int | None = Field(
        default=None,
        description="CIDR of the network that is the container of the address associated with the VM's primary interface.",
    )  # read-only
    subnet_id: str | None = Field(
        default=None,
        description="Subnet ID of the network that is the container of the address associated with the VM's primary interface.",
    )  # read-only
    tenant_name: str | None = Field(
        default=None, description="Name of the tenant associated with the VM."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    vm_type: str | None = Field(
        default=None, description="VM type; maximum 64 characters."
    )  # read-only
    vpc_address: str | None = Field(
        default=None, description="Network address of the parent VPC."
    )  # read-only
    vpc_cidr: int | None = Field(
        default=None, description="Network CIDR of the parent VPC."
    )  # read-only
    vpc_id: str | None = Field(
        default=None, description="Identifier of the parent VPC."
    )  # read-only
    vpc_name: str | None = Field(default=None, description="Name of the parent VPC.")
