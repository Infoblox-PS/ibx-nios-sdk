# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNaptr - NIOS DNS NAPTR record.

All 26 properties from ``components.schemas.RecordNaptr`` in the v2.14 DNS
swagger are represented here.  Nested types are defined inline;
``CloudInfo`` is reused from ``_shared.py``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.dns.models._shared import CloudInfo

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "creation_time",
        "dns_name",
        "dns_replacement",
        "last_queried",
        "reclaimable",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main RecordNaptr model
# ---------------------------------------------------------------------------


class RecordNaptr(BaseModel):
    """NIOS DNS NAPTR record.

    All 26 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- cloud info (reused shared type) ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common fields ---
    comment: str | None = Field(
        default=None, description="Comment for the record; maximum 256 characters."
    )  # --- read-only ---
    creation_time: int | None = Field(
        default=None, description="The time of the record creation in Epoch seconds format."
    )  # --- DDNS ---
    creator: Literal["STATIC", "DYNAMIC", "SYSTEM"] | str | None = Field(
        default=None,
        description="The record creator. Note that changing creator from or to 'SYSTEM' value is not allowed.",
    )
    ddns_principal: str | None = Field(
        default=None, description="The GSS-TSIG principal that owns this record."
    )
    ddns_protected: bool | None = Field(
        default=None,
        description="Determines if the DDNS updates for this record are allowed or not.",
    )  # --- record state ---
    disable: bool | None = Field(
        default=None,
        description="Determines if the record is disabled or not. False means that the record is enabled.",
    )  # --- read-only ---
    dns_name: str | None = Field(
        default=None, description="The name of the NAPTR record in punycode format."
    )
    dns_replacement: str | None = Field(
        default=None, description="The replacement field of the NAPTR record in punycode format."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- NAPTR-specific ---
    flags: str | None = Field(
        default=None,
        description='The flags used to control the interpretation of the fields for an NAPTR record object. Supported values for the flags field are "U", "S", "P" and "A".',
    )  # --- reclamation ---
    forbid_reclamation: bool | None = Field(
        default=None, description="Determines if the reclamation is allowed for the record or not."
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The name of the NAPTR record in FQDN format. This value can be in unicode format.",
    )  # --- NAPTR ordering ---
    order: int | None = Field(
        default=None,
        description="The order parameter of the NAPTR records. This parameter specifies the order in which the NAPTR rules are applied when multiple rules are present. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
    preference: int | None = Field(
        default=None,
        description="The preference of the NAPTR record. The preference field determines the order NAPTR records are processed when multiple records with the same order parameter are present. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )  # --- read-only ---
    reclaimable: bool | None = Field(
        default=None, description="Determines if the record is reclaimable or not."
    )  # --- NAPTR data ---
    regexp: str | None = Field(
        default=None,
        description="The regular expression-based rewriting rule of the NAPTR record. This should be a POSIX compliant regular expression, including the substitution rule and flags. Refer to RFC 2915 for the field syntax details.",
    )
    replacement: str | None = Field(
        default=None,
        description="The replacement field of the NAPTR record object. For nonterminal NAPTR records, this field specifies the next domain name to look up. This value can be in unicode format.",
    )
    services: str | None = Field(
        default=None,
        description='The services field of the NAPTR record object; maximum 128 characters. The services field contains protocol and service identifiers, such as "http+E2U" or "SIPS+D2T".',
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None,
        description="The Time to Live (TTL) value for the NAPTR record. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
    )
    use_ttl: bool | None = Field(
        default=None, description="Use flag for: ttl"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- view / zone ---
    view: str | None = Field(
        default=None,
        description='The name of the DNS view in which the record resides. Example: "external".',
    )  # --- read-only ---
    zone: str | None = Field(
        default=None,
        description='The name of the zone in which the record resides. Example: "zone.com". If a view is not specified when searching by zone, the default view is used.',
    )
