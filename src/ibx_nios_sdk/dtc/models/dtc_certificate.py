# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcCertificate - NIOS DTC certificate.

Operations: GET only (collection and by ref). All non-_ref fields are read-only.
Certificates are managed via the Dtc.add_certificate function path.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "certificate",
        "in_use",
        "uuid",
    }
)


class DtcCertificate(BaseModel):
    """NIOS DTC certificate - read-only."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    certificate: str | None = Field(
        default=None, description="Reference to underlying X509Certificate."
    )
    in_use: bool | None = Field(
        default=None, description="Determines whether the certificate is in use or not."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
