# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Snmpuser - NIOS SNMP user.

All 10 properties from ``components.schemas.Snmpuser`` in the v2.14 security
swagger are represented here.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Snmpuser(BaseModel):
    """NIOS SNMP user.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    authentication_password: str | None = Field(
        default=None,
        description="Determines an authentication password for the user. This is a write-only attribute.",
    )
    authentication_protocol: (
        Literal["NONE", "MD5", "SHA", "SHA-224", "SHA-256", "SHA-384", "SHA-512"] | str | None
    ) = Field(default=None, description="The authentication protocol to be used for this user.")
    comment: str | None = Field(
        default=None, description="A descriptive comment for the SNMPv3 User."
    )
    disable: bool | None = Field(
        default=None, description="Determines if SNMPv3 user is disabled or not."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    name: str | None = Field(default=None, description="The name of the user.")
    privacy_password: str | None = Field(
        default=None, description="Determines a password for the privacy protocol."
    )
    privacy_protocol: Literal["NONE", "DES", "AES", "AES-192", "AES-256"] | str | None = Field(
        default=None, description="The privacy protocol to be used for this user."
    )
