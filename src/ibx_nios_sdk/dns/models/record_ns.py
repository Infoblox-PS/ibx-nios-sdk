# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNs - NIOS DNS NS record.

All 13 properties from ``components.schemas.RecordNs`` in the v2.14 DNS
swagger are represented here.  The ``addresses`` field is a list of
``RecordNsAddresses`` (defined inline).  ``CloudInfo`` is reused from
``_shared.py``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import CloudInfo, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "creator",
        "dns_name",
        "last_queried",
        "policy",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# RecordNs-specific nested types (inline, not shared)
# ---------------------------------------------------------------------------


class RecordNsAddresses(_DnsNested):
    """Address entry for an NS record's ``addresses`` list.

    Corresponds to ``components.schemas.RecordNsAddresses`` (2 fields).
    """

    address: str | None = Field(default=None, description="The address of the Zone Name Server.")
    auto_create_ptr: bool | None = Field(
        default=None, description="Flag to indicate if ptr records need to be auto created."
    )  # ---------------------------------------------------------------------------


# Main RecordNs model
# ---------------------------------------------------------------------------


class RecordNs(BaseModel):
    """NIOS DNS NS record.

    All 13 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.

    Note: RecordNs has no ``extattrs`` field in the swagger schema.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    addresses: list[RecordNsAddresses] | None = Field(
        default=None, description="The list of zone name servers."
    )  # --- cloud info (reused shared type) ---
    cloud_info: CloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- read-only ---
    creator: Literal["STATIC", "SYSTEM"] | str | None = Field(
        default=None, description="The record creator."
    )
    dns_name: str | None = Field(
        default=None, description="The name of the NS record in punycode format."
    )
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- delegation info ---
    ms_delegation_name: str | None = Field(
        default=None, description="The MS delegation point name."
    )  # --- core identity ---
    name: str | None = Field(
        default=None,
        description="The name of the NS record in FQDN format. This value can be in unicode format.",
    )
    nameserver: str | None = Field(
        default=None,
        description="The domain name of an authoritative server for the redirected zone.",
    )  # --- read-only ---
    policy: str | None = Field(default=None, description="The host name policy for the record.")
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
