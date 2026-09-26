# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordCname - NIOS DTC CNAME record.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "auto_created",
        "dns_canonical",
        "uuid",
    }
)


class DtcRecordCname(BaseModel):
    """NIOS DTC CNAME record."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    auto_created: str | None = Field(
        default=None,
        description="Flag that indicates whether this record was automatically created by NIOS.",
    )
    dns_canonical: str | None = Field(
        default=None, description="The canonical name as server by DNS protocol."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    canonical: str | None = Field(default=None, description="The canonical name of the host.")
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
    ttl: int | None = Field(default=None, description="The Time to Live (TTL) value.")
    use_ttl: bool | None = Field(default=None, description="Use flag for: ttl")
