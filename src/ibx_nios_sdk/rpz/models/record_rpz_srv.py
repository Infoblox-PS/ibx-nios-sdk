# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzSrv - NIOS RPZ SRV record.

All 15 properties from ``components.schemas.RecordRpzSrv`` in the v2.14 RPZ
swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
        "zone",
    }
)


class RecordRpzSrv(BaseModel):
    """NIOS RPZ SRV record.

    All 15 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- common fields ---
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
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The name for a record in FQDN format. This value cannot be in unicode format.",
    )
    port: int | None = Field(
        default=None,
        description="The port of the Substitute (SRV Record) Rule. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
    priority: int | None = Field(
        default=None,
        description="The priority of the Substitute (SRV Record) Rule. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )  # --- RPZ zone (writable zone reference) ---
    rp_zone: str | None = Field(
        default=None, description="The name of a response policy zone in which the record resides."
    )  # --- core identity ---
    target: str | None = Field(
        default=None,
        description="The target of the Substitute (SRV Record) Rule in FQDN format. This value can be in unicode format.",
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
    )  # --- weight ---
    weight: int | None = Field(
        default=None,
        description="The weight of the Substitute (SRV Record) Rule. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )  # --- read-only ---
    zone: str | None = Field(
        default=None,
        description='The name of the zone in which the record resides. Example: "zone.com". If a view is not specified when searching by zone, the default view is used.',
    )
