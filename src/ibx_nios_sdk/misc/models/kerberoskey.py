# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Kerberoskey - NIOS Kerberos key object.

Operations: GET collection, GET by ref, DELETE (no POST/PUT).

WAPI type: kerberoskey

NOTES:
- All fields are read-only.
- 'members' is a list field.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "domain",
        "enctype",
        "in_use",
        "members",
        "principal",
        "upload_timestamp",
        "uuid",
        "version",
    }
)


class Kerberoskey(BaseModel):
    """NIOS Kerberos key."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    domain: str | None = Field(default=None, description="The Kerberos domain name.")
    enctype: (
        Literal[
            "AES128-CTS-HMAC-SHA1-96",
            "AES256-CTS-HMAC-SHA1-96",
            "ARCFOUR-HMAC-MD5",
            "DES-CBC-CRC",
            "DES-CBC-MD5",
        ]
        | str
        | None
    ) = Field(default=None, description="The Kerberos key encryption type.")
    in_use: bool | None = Field(
        default=None,
        description="Determines whether the Kerberos key is assigned to the Grid or Grid member.",
    )
    members: list[str] | None = Field(
        default=None,
        description="The list of hostnames and services of Grid members where the key is assigned or Grid/DHCP4 or Grid/DHCP6 or Grid/DNS.",
    )
    principal: str | None = Field(
        default=None, description="The principal of the Kerberos key object."
    )
    upload_timestamp: int | None = Field(
        default=None, description="The timestamp of the Kerberos key upload operation."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    version: int | None = Field(
        default=None, description="The Kerberos key version number (KVNO)."
    )
