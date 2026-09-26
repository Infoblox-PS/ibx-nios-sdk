# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapi - NIOS Grid Cloud API settings."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class GridCloudapi(BaseModel):
    """NIOS Grid Cloud API settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allow_api_admins: Literal["NONE", "LIST", "ALL"] | str | None = Field(
        default=None,
        description="Defines administrators who can perform cloud API requests on the Grid Master. The valid value is NONE (no administrator), ALL (all administrators), or LIST (administrators on the ACL).",
    )
    allowed_api_admins: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of administrators who can perform cloud API requests on the Cloud Platform Appliance.",
    )
    enable_recycle_bin: bool | None = Field(
        default=None,
        description="Determines whether the recycle bin for deleted cloud objects is enabled or not on the Grid Master.",
    )
    gateway_config: dict[str, Any] | None = Field(
        default=None, description="Cloud gateway configuration block."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
