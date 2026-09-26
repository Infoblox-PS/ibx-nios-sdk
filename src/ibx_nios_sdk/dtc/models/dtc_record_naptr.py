# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordNaptr - NIOS DTC NAPTR record.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class DtcRecordNaptr(BaseModel):
    """NIOS DTC NAPTR record."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="Comment for the record; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines if the record is disabled or not. False means that the record is enabled.",
    )
    dtc_server: str | None = Field(
        default=None,
        description="The name of the DTC Server object with which the DTC record is associated.",
    )
    flags: str | None = Field(
        default=None,
        description='The flags used to control the interpretation of the fields for an NAPTR record object. Supported values for the flags field are "U", "S", "P" and "A".',
    )
    order: int | None = Field(
        default=None,
        description="The order parameter of the NAPTR records. This parameter specifies the order in which the NAPTR rules are applied when multiple rules are present. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
    preference: int | None = Field(
        default=None,
        description="The preference of the NAPTR record. The preference field determines the order the NAPTR records are processed when multiple records with the same order parameter are present. Valid values are from 0 to 65535 (inclusive), in 32-bit unsigned integer format.",
    )
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
    )
    ttl: int | None = Field(default=None, description="The Time to Live (TTL) value.")
    use_ttl: bool | None = Field(default=None, description="Use flag for: ttl")
