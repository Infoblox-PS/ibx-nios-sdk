# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordA - NIOS DNS shared A record.

All 11 properties from ``components.schemas.SharedrecordA`` in the v2.14 DNS
swagger are represented here.  Shared records are much smaller than their
non-shared counterparts; no DiscoveredData or MsAdUserData nested types.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "dns_name",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main SharedrecordA model
# ---------------------------------------------------------------------------


class SharedrecordA(BaseModel):
    """NIOS DNS shared A record.

    All 11 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- common fields ---
    comment: str | None = Field(
        default=None, description="Comment for this shared record; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines if this shared record is disabled or not. False means that the record is enabled.",
    )  # --- read-only ---
    dns_name: str | None = Field(
        default=None, description="The name for this shared record in punycode format."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- core identity ---
    ipv4addr: str | None = Field(
        default=None, description="The IPv4 Address of the shared record."
    )
    name: str | None = Field(
        default=None,
        description="Name for this shared record. This value can be in unicode format.",
    )  # --- shared record group reference (required on create) ---
    shared_record_group: str | None = Field(
        default=None,
        description="The name of the shared record group in which the record resides.",
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for this shared record. A 32-bit unsigned integer that represents the duration, in seconds, for which the shared record is valid (cached). Zero indicates that the shared record should not be cached.",
    )
    use_ttl: bool | None = Field(
        default=None, description="Use flag for: ttl"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
