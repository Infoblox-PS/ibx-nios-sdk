# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiTenant - NIOS Grid Cloud API tenant."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "created_ts",
        "id",
        "last_event_ts",
        "network_count",
        "uuid",
        "vm_count",
    }
)


class GridCloudapiTenant(BaseModel):
    """NIOS Grid Cloud API tenant."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )
    comment: str | None = Field(
        default=None,
        description="Comment for the Grid Cloud API Tenant object; maximum 256 characters.",
    )  # read-only
    created_ts: int | None = Field(
        default=None, description="The timestamp when the tenant was first created in the system."
    )  # read-only
    id: str | None = Field(
        default=None,
        description="Unique ID associated with the tenant. This is set only when the tenant is first created.",
    )  # read-only
    last_event_ts: int | None = Field(
        default=None,
        description="The timestamp when the last event associated with the tenant happened.",
    )
    name: str | None = Field(default=None, description="Name of the tenant.")  # read-only
    network_count: int | None = Field(
        default=None, description="Number of Networks associated with the tenant."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # read-only
    vm_count: int | None = Field(
        default=None, description="Number of VMs associated with the tenant."
    )
