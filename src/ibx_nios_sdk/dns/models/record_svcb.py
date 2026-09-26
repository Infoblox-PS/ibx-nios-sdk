# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordSvcb - NIOS DNS SVCB record.

All 22 properties from ``components.schemas.RecordSvcb`` in the v2.14 DNS
swagger are represented here.  Nested types are defined inline;
``CloudInfo`` is reused from ``_shared.py``.

NOTE: ``svc_parameters`` is typed as ``list[dict[str, Any]] | None`` because
the swagger schema uses a complex structured SvcParam array type that varies
per key code.  See NOTES.md (svcb/https params are complex structured types).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.dns.models._shared import CloudInfo, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "aws_rte53_record_info",
        "cloud_info",
        "creation_time",
        "last_queried",
        "reclaimable",
        "uuid",
        "zone",
    }
)


# ---------------------------------------------------------------------------
# RecordSvcb-specific nested types (inline, not shared)
# ---------------------------------------------------------------------------


class RecordSvcbAwsRte53RecordInfo(_DnsNested):
    """AWS Route 53 record metadata attached to a SVCB record."""

    alias_target_dns_name: str | None = Field(
        default=None, description="DNS name of the alias target."
    )
    alias_target_hosted_zone_id: str | None = Field(
        default=None, description="Hosted zone ID of the alias target."
    )
    alias_target_evaluate_target_health: bool | None = Field(
        default=None,
        description="Indicates if Amazon Route 53 evaluates the health of the alias target.",
    )
    failover: Literal["PRIMARY", "SECONDARY"] | str | None = Field(
        default=None,
        description="Indicates whether this is the primary or secondary resource record for Amazon Route 53 failover routing.",
    )
    geolocation_continent_code: str | None = Field(
        default=None, description="Continent code for Amazon Route 53 geolocation routing."
    )
    geolocation_country_code: str | None = Field(
        default=None, description="Country code for Amazon Route 53 geolocation routing."
    )
    geolocation_subdivision_code: str | None = Field(
        default=None, description="Subdivision code for Amazon Route 53 geolocation routing."
    )
    health_check_id: str | None = Field(
        default=None,
        description="ID of the health check that Amazon Route 53 performs for this resource record.",
    )
    region: str | None = Field(
        default=None,
        description="Amazon EC2 region where this resource record resides for latency routing.",
    )
    set_identifier: str | None = Field(
        default=None,
        description="An identifier that differentiates records with the same DNS name and type for weighted, latency, geolocation, and failover routing.",
    )
    type: (
        Literal["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SPF", "SRV", "TXT"] | str | None
    ) = Field(default=None, description="Type of Amazon Route 53 resource record.")
    weight: int | None = Field(
        default=None,
        description="Value that determines the portion of traffic for this record in weighted routing. The range is from 0 to 255.",
    )  # ---------------------------------------------------------------------------


# Main RecordSvcb model
# ---------------------------------------------------------------------------


class RecordSvcb(BaseModel):
    """NIOS DNS SVCB record.

    All 22 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.

    ``svc_parameters`` is approximated as ``list[dict[str, Any]] | None``; see
    module docstring for rationale.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- AWS Route 53 info ---
    aws_rte53_record_info: RecordSvcbAwsRte53RecordInfo | None = Field(
        default=None, description="AWS Route53 record info populated by Route53 sync."
    )  # --- cloud info (reused shared type) ---
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
        description="Determines if the record is disabled or not.False means that the record is enabled.",
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
        description="The name for a SVCB record in FQDN format. This value can be in unicode format. Regular expression search is not supported for unicode values.",
    )  # --- SVCB-specific ---
    priority: int | None = Field(
        default=None,
        description="The priority of the SVCB record. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )  # --- read-only ---
    reclaimable: bool | None = Field(
        default=None, description="Determines if the record is reclaimable or not."
    )  # --- svc_parameters: complex structured type, approximated ---
    svc_parameters: list[dict[str, Any]] | None = Field(
        default=None, description="Structure to represent SVC Params."
    )  # --- target ---
    target_name: str | None = Field(
        default=None,
        description="Target name in FQDN format. This value can be in unicode format.",
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
    )  # --- view / zone ---
    view: str | None = Field(
        default=None,
        description='The name of the DNS view in which the record resides. Example: "external".',
    )  # --- read-only ---
    zone: str | None = Field(
        default=None,
        description='The name of the zone in which the record resides. Example: "zone.com". If a view is not specified when searching by zone, the default view is used.',
    )
