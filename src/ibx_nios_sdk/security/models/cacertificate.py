# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Cacertificate - NIOS CA certificate (read-only).

All 8 properties from ``components.schemas.Cacertificate`` in the v2.14
security swagger are represented here. All non-_ref fields are readOnly.

Operations: GET collection, GET by ref (read-only aggregate - no write ops).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "distinguished_name",
        "issuer",
        "serial",
        "used_by",
        "uuid",
        "valid_not_after",
        "valid_not_before",
    }
)


class Cacertificate(BaseModel):
    """NIOS CA certificate.

    All fields are read-only. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    distinguished_name: str | None = Field(
        default=None, description="The certificate subject name."
    )
    issuer: str | None = Field(default=None, description="The certificate issuer subject name.")
    serial: str | None = Field(
        default=None, description="The certificate serial number in hex format."
    )
    used_by: str | None = Field(
        default=None, description="Information about the CA certificate usage."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_not_after: int | None = Field(
        default=None, description="The date after which the certificate becomes invalid."
    )
    valid_not_before: int | None = Field(
        default=None, description="The date before which the certificate is not valid."
    )
