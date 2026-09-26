# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverDns - NIOS MS server DNS.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "uuid",
    }
)


class MsserverDns(BaseModel):
    """NIOS MS server DNS."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    address: str | None = Field(
        default=None, description="The address or FQDN of the DNS Microsoft Server."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    enable_dns_reports_sync: bool | None = Field(
        default=None,
        description="Determines if synchronization of DNS reporting data from the Microsoft server is enabled or not.",
    )
    login_name: str | None = Field(
        default=None, description="The login name of the DNS Microsoft Server."
    )
    login_password: str | None = Field(
        default=None, description="The login password of the DNS Microsoft Server."
    )
    synchronization_interval: int | None = Field(
        default=None, description="The minimum number of minutes between two synchronizations."
    )
    use_enable_dns_reports_sync: bool | None = Field(
        default=None, description="Use flag for: enable_dns_reports_sync"
    )
    use_login: bool | None = Field(
        default=None, description="Use flag for: login_name , login_password"
    )
    use_synchronization_interval: bool | None = Field(
        default=None, description="Use flag for: synchronization_interval"
    )
