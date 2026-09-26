# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Networkuser - NIOS network user.

All 17 properties from ``components.schemas.Networkuser`` in the v2.14 security
swagger are represented here.

Note: ``user_status`` is readOnly even though the plan listed it in
default_return_fields. It is included as a readable field on GET responses but
stripped on PUT/POST. See NOTES.md.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address_object",
        "data_source",
        "data_source_ip",
        "network",
        "user_status",
        "uuid",
    }
)


class Networkuser(BaseModel):
    """NIOS network user.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    address_object: str | None = Field(
        default=None,
        description="The reference of the IPAM IPv4Address or IPv6Address object describing the address of the Network User.",
    )
    data_source: str | None = Field(default=None, description="The Network User data source.")
    data_source_ip: str | None = Field(
        default=None,
        description="The Network User data source IPv4 Address or IPv6 Address or FQDN address.",
    )
    network: str | None = Field(
        default=None, description="The reference to the network to which the Network User belongs."
    )
    user_status: Literal["ACTIVE", "LOGOUT", "TIMEOUT"] | str | None = Field(
        default=None, description="The status of the Network User."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    address: str | None = Field(
        default=None, description="The IPv4 Address or IPv6 Address of the Network User."
    )
    domainname: str | None = Field(
        default=None, description="The domain name of the Network User."
    )
    first_seen_time: int | None = Field(
        default=None, description="The first seen timestamp of the Network User."
    )
    guid: str | None = Field(default=None, description="The group identifier of the Network User.")
    last_seen_time: int | None = Field(
        default=None, description="The last seen timestamp of the Network User."
    )
    last_updated_time: int | None = Field(
        default=None, description="The last updated timestamp of the Network User."
    )
    logon_id: str | None = Field(
        default=None, description="The logon identifier of the Network User."
    )
    logout_time: int | None = Field(
        default=None, description="The logout timestamp of the Network User."
    )
    name: str | None = Field(default=None, description="The name of the Network User.")
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which this Network User resides.",
    )
