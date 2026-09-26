# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Allrpzrecords - NIOS RPZ aggregate read-only object.

All 13 properties from ``components.schemas.Allrpzrecords`` in the v2.14 RPZ
swagger are represented here.  12 of the 13 non-``_ref`` properties are
read-only.  This is a read-only aggregate - list/get only, no write operations.

Note: ``type`` is a Python keyword-collision; it is aliased as ``type_`` with
``Field(alias="type")``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - all non-_ref fields
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "alert_type",
        "comment",
        "disable",
        "expiration_time",
        "last_updated",
        "name",
        "record",
        "rpz_rule",
        "ttl",
        "type",
        "type_",
        "view",
        "zone",
    }
)


class Allrpzrecords(BaseModel):
    """NIOS RPZ aggregate - read-only view across all RPZ record types.

    All 12 non-``_ref`` swagger properties are present and read-only.
    ``type`` (Python keyword collision) is exposed as ``type_`` with
    ``Field(alias="type")``.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    alert_type: (
        Literal[
            "INFECTION_MATCH",
            "WEB_INFECTION",
            "MALWARE_OBJECT",
            "DOMAIN_MATCH",
            "MALWARE_CALLBACK",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The alert type of the record associated with the allrpzrecords object.",
    )
    comment: str | None = Field(
        default=None,
        description="The descriptive comment of the record associated with the allrpzrecords object.",
    )
    disable: bool | None = Field(
        default=None,
        description="The disable flag of the record associated with the allrpzrecords object (if present).",
    )
    expiration_time: int | None = Field(
        default=None,
        description="The expiration time of the record associated with the allrpzrecords object.",
    )
    last_updated: int | None = Field(
        default=None,
        description="The time when the record associated with the allrpzrecords object was last updated.",
    )
    name: str | None = Field(
        default=None,
        description="The name of the record associated with the allrpzrecords object. Note that this value might be different than the value of the name field for the associated record.",
    )
    record: str | None = Field(
        default=None, description="The record object associated with the allrpzrecords object."
    )
    rpz_rule: (
        Literal[
            "BlockNoDataClientIpaddr",
            "BlockNoDataDomain",
            "BlockNoDataIpaddr",
            "BlockNxdomainClientIpaddr",
            "BlockNxdomainDomain",
            "BlockNxdomainIpaddr",
            "PassthruClientIpaddr",
            "PassthruDomain",
            "PassthruIpaddr",
            "SubstituteAAAARecord",
            "SubstituteARecord",
            "SubstituteCName",
            "SubstituteClientIPAddressCname",
            "SubstituteHTTPSRecord",
            "SubstituteIPAddressCname",
            "SubstituteIPv4AddressRecord",
            "SubstituteIPv6AddressRecord",
            "SubstituteMXRecord",
            "SubstituteNAPTRRecord",
            "SubstitutePTRRecord",
            "SubstituteSRVRecord",
            "SubstituteSVCBRecord",
            "SubstituteTXTRecord",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The RPZ rule type of the record associated with the allrpzrecrods object.",
    )
    ttl: int | None = Field(
        default=None,
        description="The TTL value of the record associated with the allrpzrecords object (if present).",
    )  # --- Python keyword collision: type → type_ ---
    type_: (
        Literal[
            "record:rpz:a",
            "record:rpz:a:ipaddress",
            "record:rpz:aaaa",
            "record:rpz:aaaa:ipaddress",
            "record:rpz:cname",
            "record:rpz:cname:clientipaddress",
            "record:rpz:cname:ipaddress",
            "record:rpz:cname:ipaddressdn",
            "record:rpz:https",
            "record:rpz:mx",
            "record:rpz:naptr",
            "record:rpz:ptr",
            "record:rpz:srv",
            "record:rpz:svcb",
            "record:rpz:txt",
        ]
        | str
        | None
    ) = Field(default=None, alias="type", description="Object type discriminator.")

    view: str | None = Field(
        default=None,
        description="The DNS view name of the record associated with the allrpzrecords object.",
    )
    zone: str | None = Field(
        default=None,
        description="The Response Policy Zone name of the record associated with the allrpzrecords object.",
    )
