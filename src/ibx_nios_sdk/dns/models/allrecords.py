# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Allrecords - NIOS DNS aggregate all-records list (read-only).

All 15 properties from ``components.schemas.Allrecords`` in the v2.14 DNS
swagger are represented here.  This object is a read-only aggregate; every
field except ``_ref`` is marked readOnly in swagger.  The ``type`` field
conflicts with a Python builtin so it is aliased as ``type_``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# All non-_ref fields are read-only for this aggregate object.
# Note: the ``type`` WAPI field is stored as Python field ``type_``; the
# exclude set uses Python field names (not aliases) because WapiResource calls
# ``model_dump(exclude=_readonly_fields)``.
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "comment",
        "creator",
        "ddns_principal",
        "ddns_protected",
        "disable",
        "dtc_obscured",
        "name",
        "reclaimable",
        "record",
        "ttl",
        "type",
        "type_",
        "view",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# Main Allrecords model
# ---------------------------------------------------------------------------


class Allrecords(BaseModel):
    """NIOS DNS aggregate all-records (read-only list resource).

    ``type_`` is aliased to the WAPI field ``type`` to avoid shadowing the
    Python builtin.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only fields ---
    address: str | None = Field(default=None, description="The record address.")  # RO
    comment: str | None = Field(default=None, description="The record comment.")  # RO
    creator: Literal["STATIC", "DYNAMIC", "SYSTEM"] | str | None = Field(
        default=None, description="The record creator."
    )  # RO
    ddns_principal: str | None = Field(
        default=None, description="The GSS-TSIG principal that owns this record."
    )  # RO
    ddns_protected: bool | None = Field(
        default=None,
        description="Determines if the DDNS updates for this record are allowed or not.",
    )  # RO
    disable: bool | None = Field(
        default=None,
        description='The disable value determines if the record is disabled or not. "False" means the record is enabled.',
    )  # RO
    dtc_obscured: str | None = Field(default=None, description="The specific LBDN record.")  # RO
    name: str | None = Field(default=None, description="The name of the record.")  # RO
    reclaimable: bool | None = Field(
        default=None, description="Determines if the record is reclaimable or not."
    )  # RO
    record: str | None = Field(
        default=None,
        description='The record object, if supported by the WAPI. Otherwise, the value is "None".',
    )  # RO
    ttl: int | None = Field(
        default=None,
        description="The Time To Live (TTL) value for which the record is valid or being cached. The 32-bit unsigned integer represents the duration in seconds. Zero indicates that the record should not be cached.",
    )  # RO
    type_: (
        Literal[
            "ALL",
            "record:a",
            "record:aaaa",
            "record:cname",
            "record:dname",
            "record:host",
            "record:host_ipv4addr",
            "record:host_ipv6addr",
            "record:https",
            "record:mx",
            "record:naptr",
            "record:ptr",
            "record:srv",
            "record:svcb",
            "record:txt",
            "record:unknown",
            "sharedrecord:a",
            "sharedrecord:aaaa",
            "sharedrecord:mx",
            "sharedrecord:srv",
            "sharedrecord:txt",
        ]
        | str
        | None
    ) = Field(default=None, alias="type", description="Object type discriminator.")  # RO
    view: str | None = Field(
        default=None, description="Name of the DNS View in which the record resides."
    )  # RO
    zone: str | None = Field(
        default=None, description="Name of the zone in which the record resides."
    )  # RO
