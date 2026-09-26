# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordUnknown - NIOS DNS unknown/generic record type.

All 19 properties from ``components.schemas.RecordUnknown`` in the v2.14 DNS
swagger are represented here.  Nested types are defined inline;
``CloudInfo`` is reused from ``_shared.py``.

NOTE: ``subfield_values`` is typed as ``list[dict[str, Any]] | None`` because
the swagger schema uses a complex per-record-type structure.  See NOTES.md.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.dns.models._shared import CloudInfo

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "display_rdata",
        "dns_name",
        "last_queried",
        "policy",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main RecordUnknown model
# ---------------------------------------------------------------------------


class RecordUnknown(BaseModel):
    """NIOS DNS unknown/generic record type.

    All 19 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.

    ``subfield_values`` is approximated as ``list[dict[str, Any]] | None``; see
    module docstring for rationale.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- cloud info (reused shared type) ---
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
    display_rdata: str | None = Field(
        default=None, description="Standard textual representation of the RDATA."
    )
    dns_name: str | None = Field(
        default=None, description="The name of the unknown record in punycode format."
    )  # --- hostname policy ---
    enable_host_name_policy: bool | None = Field(
        default=None, description="Determines if host name policy is applicable for the record."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The Unknown record name in FQDN format. This value can be in unicode format.",
    )  # --- read-only ---
    policy: str | None = Field(
        default=None, description="The host name policy for the record."
    )  # --- record type identifier ---
    record_type: str | None = Field(
        default=None, description="Specifies type of unknown resource record."
    )  # --- subfield_values: complex per-type structure, approximated ---
    subfield_values: list[dict[str, Any]] | None = Field(
        default=None, description="The list of rdata subfield values of unknown resource record."
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
