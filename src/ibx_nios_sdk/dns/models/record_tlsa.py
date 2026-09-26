# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordTlsa - NIOS DNS TLSA record.

All 18 properties from ``components.schemas.RecordTlsa`` in the v2.14 DNS
swagger are represented here.  Nested types are defined inline;
``CloudInfo`` is reused from ``_shared.py``.

NOTE: WAPI names the TLSA matching-type integer field ``matched_type``. Earlier
releases aliased it to ``matching_type``, which made create/update send a field
name NIOS does not know; the alias was removed.
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
        "dns_name",
        "last_queried",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main RecordTlsa model
# ---------------------------------------------------------------------------


class RecordTlsa(BaseModel):
    """NIOS DNS TLSA record.

    All 18 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.

    The WAPI field name is ``matched_type``.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- certificate data ---
    certificate_data: str | None = Field(
        default=None,
        description="Hex dump of either raw data for matching type 0, or the hash of the raw data for matching types 1 and 2.",
    )
    certificate_usage: int | None = Field(
        default=None,
        description="Specifies the provided association that will be used to match the certificate presented in the TLS handshake. Based on RFC-6698.",
    )  # --- cloud info (reused shared type) ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common fields ---
    comment: str | None = Field(
        default=None, description="Comment for the record; maximum 256 characters."
    )  # --- DDNS ---
    creator: Literal["STATIC", "DYNAMIC", "SYSTEM"] | str | None = Field(
        default=None,
        description="The record creator. Note that changing creator from or to 'SYSTEM' value is not allowed.",
    )  # --- record state ---
    disable: bool | None = Field(
        default=None,
        description="Determines if the record is disabled or not. False means that the record is enabled.",
    )  # --- read-only ---
    dns_name: str | None = Field(
        default=None, description="The name of the TLSA record in punycode format."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- TLSA matching type (WAPI: matched_type) ---
    matched_type: int | None = Field(
        default=None,
        description="Specifies how the certificate association is presented. Based on RFC-6698.",
    )

    # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The TLSA record name in FQDN format. This value can be in unicode format.",
    )  # --- TLSA selector ---
    selector: int | None = Field(
        default=None,
        description="Specifies which part of the TLS certificate presented by the server will be matched against the association data. Based on RFC-6698.",
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None,
        description="The Time to Live (TTL) value for the record. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
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
