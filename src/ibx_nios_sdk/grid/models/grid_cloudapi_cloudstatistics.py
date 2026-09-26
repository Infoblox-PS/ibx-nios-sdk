# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiCloudstatistics - NIOS Grid Cloud API statistics (all read-only)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "allocated_available_ratio",
        "allocated_ip_count",
        "available_ip_count",
        "fixed_ip_count",
        "floating_ip_count",
        "tenant_count",
        "tenant_ip_count",
        "tenant_vm_count",
    }
)


class GridCloudapiCloudstatistics(BaseModel):
    """NIOS Grid Cloud API statistics."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    allocated_available_ratio: float | None = Field(
        default=None, description="Ratio of allocated vs. available IPs"
    )
    allocated_ip_count: int | None = Field(
        default=None, description="Total number of IPs allocated by tenants."
    )
    available_ip_count: str | None = Field(
        default=None,
        description="The total number of IP addresses available to tenants. Only IP addresses in networks that are within a delegation scope are counted.",
    )
    fixed_ip_count: int | None = Field(
        default=None,
        description="The total number of fixed IP addresses currently in use by all tenants in the system.",
    )
    floating_ip_count: int | None = Field(
        default=None,
        description="The total number of floating IP addresses currently in use by all tenants in the system.",
    )
    tenant_count: int | None = Field(
        default=None, description="Total number of tenant currently in the system."
    )
    tenant_ip_count: int | None = Field(
        default=None,
        description="The total number of IP addresses currently in use by all tenants in the system.",
    )
    tenant_vm_count: int | None = Field(
        default=None,
        description="The total number of VMs currently in use by all tenants in the system.",
    )
