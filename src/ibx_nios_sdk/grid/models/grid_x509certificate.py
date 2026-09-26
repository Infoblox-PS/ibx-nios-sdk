# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridX509certificate - NIOS Grid X.509 certificate."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "issuer",
        "serial",
        "subject",
        "uuid",
        "valid_not_after",
        "valid_not_before",
    }
)


class GridX509certificate(BaseModel):
    """NIOS Grid X.509 certificate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    issuer: str | None = Field(default=None, description="Certificate issuer.")  # read-only
    serial: str | None = Field(
        default=None, description="X509Certificate serial number."
    )  # read-only
    subject: str | None = Field(
        default=None,
        description="A Distinguished Name that is made of multiple relative distinguished names (RDNs).",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # read-only
    valid_not_after: int | None = Field(
        default=None, description="Certificate expiry date."
    )  # read-only
    valid_not_before: int | None = Field(
        default=None, description="Certificate validity start date."
    )
