# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordSrv - NIOS DTC SRV record.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class DtcRecordSrv(BaseModel):
    """NIOS DTC SRV record."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="Comment for the record; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines if the record is disabled or not. False means that the record is enabled.",
    )
    dtc_server: str | None = Field(
        default=None,
        description="The name of the DTC Server object with which the DTC record is associated.",
    )
    name: str | None = Field(
        default=None, description="The name for an SRV record in unicode format."
    )
    port: int | None = Field(
        default=None,
        description="The port of the SRV record. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
    priority: int | None = Field(
        default=None,
        description="The priority of the SRV record. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
    target: str | None = Field(
        default=None,
        description="The target of the SRV record in FQDN format. This value can be in unicode format.",
    )
    ttl: int | None = Field(default=None, description="The Time to Live (TTL) value.")
    use_ttl: bool | None = Field(default=None, description="Use flag for: ttl")
    weight: int | None = Field(
        default=None,
        description="The weight of the SRV record. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
