# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridMemberCloudapi - NIOS per-member Cloud API settings.

NOTE: WAPI type is ``grid:member:cloudapi`` (path /grid:member:cloudapi).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "extattrs",
        "member",
        "status",
        "uuid",
    }
)


class GridMemberCloudapi(BaseModel):
    """NIOS per-member Cloud API settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allow_api_admins: Literal["NONE", "LIST", "ALL"] | str | None = Field(
        default=None,
        description="Defines which administrators are allowed to perform Cloud API request on the Grid Member: no administrators (NONE), any administrators (ALL) or administrators in the ACL list (LIST). Default is ALL.",
    )
    allowed_api_admins: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of administrators allowed to perform Cloud Platform API requests on that member.",
    )
    enable_service: bool | None = Field(
        default=None,
        description="Controls whether the Cloud API service runs on the member or not.",
    )  # read-only
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    gateway_config: dict[str, Any] | None = Field(
        default=None, description="Cloud gateway configuration block."
    )
    member: dict[str, Any] | None = Field(
        default=None, description="The name of the updates download member."
    )  # read-only
    status: Literal["UNKNOWN", "INACTIVE", "WORKING", "WARNING", "FAILED"] | str | None = Field(
        default=None, description="Status of Cloud API service on the member."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
