# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDhcid - NIOS DNS DHCID record.

All 11 properties from ``components.schemas.RecordDhcid`` in the v2.14 DNS
swagger are represented here.

NOTE: All 10 non-_ref fields are read-only (readOnly: true in swagger).
DHCID records are created automatically by NIOS DHCP and cannot be created
or modified via the WAPI; they can only be queried and deleted.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - all substantive fields
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "creation_time",
        "creator",
        "dhcid",
        "dns_name",
        "name",
        "ttl",
        "use_ttl",
        "uuid",
        "view",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main RecordDhcid model
# ---------------------------------------------------------------------------


class RecordDhcid(BaseModel):
    """NIOS DNS DHCID record.

    All 11 swagger properties are present.  All substantive fields are
    read-only (set by NIOS DHCP automatically).  See :data:`READONLY_FIELDS`.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- all fields are read-only ---
    creation_time: int | None = Field(default=None, description="The creation time of the record.")
    creator: Literal["SYSTEM", "STATIC", "DYNAMIC"] | str | None = Field(
        default=None, description="The record creator."
    )
    dhcid: str | None = Field(
        default=None, description="The Base64 encoded DHCP client information."
    )
    dns_name: str | None = Field(
        default=None, description="The name for the DHCID record in punycode format."
    )
    name: str | None = Field(
        default=None, description="The name of the DHCID record in FQDN format."
    )
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for the record. A 32-bit unsigned integer that represents the duration, in seconds, for which the record is valid (cached). Zero indicates that the record should not be cached.",
    )
    use_ttl: bool | None = Field(default=None, description="Use flag for: ttl")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    view: str | None = Field(
        default=None,
        description='The name of the DNS view in which the record resides. Example: "external".',
    )
    zone: str | None = Field(
        default=None,
        description='The name of the zone in which the record resides. Example: "zone.com". If a view is not specified when searching by zone, the default view is used.',
    )
