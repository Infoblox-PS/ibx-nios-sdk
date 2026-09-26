# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordCaa - NIOS DNS CAA record.

All 22 properties from ``components.schemas.RecordCaa`` in the v2.14 DNS
swagger are represented here.  Nested types are defined inline;
``CloudInfo`` is reused from ``_shared.py``.

NOTE: The swagger uses ``ca_flag``, ``ca_tag``, ``ca_value`` for the three
CAA record data fields.  The plan's default_return_fields table lists
``flag``, ``tag``, ``ca_value`` - we use the swagger names (ca_flag, ca_tag,
ca_value) as the canonical field names since those match the WAPI wire format.
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
        "last_queried",
        "reclaimable",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main RecordCaa model
# ---------------------------------------------------------------------------


class RecordCaa(BaseModel):
    """NIOS DNS CAA record.

    All 22 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- CAA data ---
    ca_flag: int | None = Field(default=None, description="Flag of CAA record.")
    ca_tag: str | None = Field(default=None, description="Tag of CAA record.")
    ca_value: str | None = Field(
        default=None, description="Value of CAA record"
    )  # --- cloud info (reused shared type) ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common fields ---
    comment: str | None = Field(
        default=None, description="Comment for the record; maximum 256 characters."
    )  # --- read-only ---
    creation_time: int | None = Field(
        default=None, description="The creation time of the record."
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
        default=None, description="The name of the CAA record in punycode format."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- reclamation ---
    forbid_reclamation: bool | None = Field(
        default=None, description="Determines if the reclamation is allowed for the record or not."
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The CAA record name in FQDN format. This value can be in unicode format.",
    )  # --- read-only ---
    reclaimable: bool | None = Field(
        default=None, description="Determines if the record is reclaimable or not."
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
