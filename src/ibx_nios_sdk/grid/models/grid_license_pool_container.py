# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridLicensePoolContainer - NIOS Grid license pool container."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "last_entitlement_update",
        "lpc_uid",
        "uuid",
    }
)


class GridLicensePoolContainer(BaseModel):
    """NIOS Grid license pool container."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allocate_licenses: dict[str, object] | None = Field(default=None)  # read-only
    last_entitlement_update: int | None = Field(
        default=None, description="The timestamp when the last pool licenses were updated."
    )  # read-only
    lpc_uid: str | None = Field(
        default=None, description="The world-wide unique ID for the license pool container."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
