# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzNaptr - NIOS RPZ NAPTR record.

All 18 properties from ``components.schemas.RecordRpzNaptr`` in the v2.14 RPZ
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
        "last_queried",
        "uuid",
        "zone",
    }
)


class RecordRpzNaptr(BaseModel):
    """NIOS RPZ NAPTR record.

    All 18 swagger properties are present.  Read-only fields are collected in
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
    )  # --- NAPTR fields ---
    flags: str | None = Field(
        default=None,
        description='The flags used to control the interpretation of the fields for a Substitute (NAPTR Record) Rule object. Supported values for the flags field are "U", "S", "P" and "A".',
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The name for a record in FQDN format. This value cannot be in unicode format.",
    )
    order: int | None = Field(
        default=None,
        description="The order parameter of the Substitute (NAPTR Record) Rule records. This parameter specifies the order in which the NAPTR rules are applied when multiple rules are present. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
    preference: int | None = Field(
        default=None,
        description="The preference of the Substitute (NAPTR Record) Rule record. The preference field determines the order NAPTR records are processed when multiple records with the same order parameter are present. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
    regexp: str | None = Field(
        default=None,
        description="The regular expression-based rewriting rule of the Substitute (NAPTR Record) Rule record. This should be a POSIX compliant regular expression, including the substitution rule and flags. Refer to RFC 2915 for the field syntax details.",
    )
    replacement: str | None = Field(
        default=None,
        description="The replacement field of the Substitute (NAPTR Record) Rule object. For nonterminal NAPTR records, this field specifies the next domain name to look up. This value can be in unicode format.",
    )  # --- RPZ zone (writable zone reference) ---
    rp_zone: str | None = Field(
        default=None, description="The name of a response policy zone in which the record resides."
    )  # --- NAPTR service ---
    services: str | None = Field(
        default=None,
        description='The services field of the Substitute (NAPTR Record) Rule object; maximum 128 characters. The services field contains protocol and service identifiers, such as "http+E2U" or "SIPS+D2T".',
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
