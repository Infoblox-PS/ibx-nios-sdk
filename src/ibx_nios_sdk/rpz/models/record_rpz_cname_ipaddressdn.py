# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzCnameIpaddressdn - NIOS RPZ CNAME:Ipaddressdn record.

All 13 properties from ``components.schemas.RecordRpzCnameIpaddressdn`` in
the v2.14 RPZ swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "is_ipv4",
        "uuid",
        "zone",
    }
)


class RecordRpzCnameIpaddressdn(BaseModel):
    """NIOS RPZ CNAME:Ipaddressdn record.

    All 13 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    canonical: str | None = Field(
        default=None,
        description="The canonical name in FQDN format. This value can be in unicode format.",
    )  # --- common fields ---
    comment: str | None = Field(
        default=None, description="The comment for the record; maximum 256 characters."
    )  # --- record state ---
    disable: bool | None = Field(
        default=None,
        description="Determines if the record is disabled or not. False means that the record is enabled.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- read-only ---
    is_ipv4: bool | None = Field(
        default=None,
        description='Indicates whether the record is an IPv4 record. If the return value is "true", it is an IPv4 record. Otherwise, it is an IPv6 record.',
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The name for a record in FQDN format. This value cannot be in unicode format.",
    )  # --- RPZ zone (writable zone reference) ---
    rp_zone: str | None = Field(
        default=None, description="The name of a response policy zone in which the record resides."
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for record. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
    )
    use_ttl: bool | None = Field(
        default=None, description="Use flag for: ttl"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- view ---
    view: str | None = Field(
        default=None,
        description='The name of the DNS View in which the record resides. Example: "external".',
    )  # --- read-only ---
    zone: str | None = Field(
        default=None,
        description='The name of the zone in which the record resides. Example: "zone.com". If a view is not specified when searching by zone, the default view is used.',
    )
