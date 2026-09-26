# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDname - NIOS DNS DNAME record.

All 22 properties from ``components.schemas.RecordDname`` in the v2.14 DNS
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
        "dns_target",
        "last_queried",
        "reclaimable",
        "shared_record_group",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main RecordDname model
# ---------------------------------------------------------------------------


class RecordDname(BaseModel):
    """NIOS DNS DNAME record.

    All 22 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- cloud info (reused shared type) ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common fields ---
    comment: str | None = Field(
        default=None, description="The comment for the record."
    )  # --- read-only ---
    creation_time: int | None = Field(
        default=None, description="The time of the record creation in Epoch seconds format."
    )  # --- DDNS ---
    creator: Literal["STATIC", "DYNAMIC", "SYSTEM"] | str | None = Field(
        default=None, description="The record creator."
    )
    ddns_principal: str | None = Field(
        default=None, description="The GSS-TSIG principal that owns this record."
    )
    ddns_protected: bool | None = Field(
        default=None, description="Determines if the DDNS updates for this record are allowed."
    )  # --- record state ---
    disable: bool | None = Field(
        default=None, description="Determines if the record is disabled."
    )  # --- read-only ---
    dns_name: str | None = Field(
        default=None, description="Name of a DNS DNAME record in punycode format."
    )
    dns_target: str | None = Field(
        default=None,
        description="The target domain name of the DNS DNAME record in punycode format.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- reclamation ---
    forbid_reclamation: bool | None = Field(
        default=None, description="Determines if reclamation is allowed for the record."
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- core identity ---
    name: str | None = Field(
        default=None, description="The name of the DNS DNAME record in FQDN format."
    )  # --- read-only ---
    reclaimable: bool | None = Field(
        default=None, description="Determines if the record is reclaimable."
    )  # --- read-only ---
    shared_record_group: str | None = Field(
        default=None,
        description="The name of the shared record group in which the record resides. This field exists only on db_objects if this record is a shared record.",
    )  # --- target ---
    target: str | None = Field(
        default=None, description="The target domain name of the DNS DNAME record in FQDN format."
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None,
        description="Time To Live (TTL) value for the record. A 32-bit unsigned integer that represents the duration, in seconds, that the record is valid (cached). Zero indicates that the record should not be cached.",
    )
    use_ttl: bool | None = Field(
        default=None, description="Use flag for: ttl"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- view / zone ---
    view: str | None = Field(
        default=None,
        description='The name of the DNS View in which the record resides, for example "external".',
    )  # --- read-only ---
    zone: str | None = Field(
        default=None,
        description='The name of the zone in which the record resides. For example: "zone.com". If a view is not specified when searching by zone, the default view is used.',
    )
