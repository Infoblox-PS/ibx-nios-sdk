# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Superhostchild - NIOS IPAM superhost child object.

All 12 properties from ``components.schemas.Superhostchild`` in the v2.14
IPAM swagger are represented here. All non-ref fields are read-only.

NOTE: In practice this is a read-only view object; WAPI will reject most
write attempts. No SDK enforcement - callers are responsible.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - all non-ref fields are RO
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "associated_object",
        "comment",
        "creation_timestamp",
        "data",
        "disabled",
        "name",
        "network_view",
        "parent",
        "record_parent",
        "type",
        "view",
    }
)


# ---------------------------------------------------------------------------
# Main Superhostchild model
# ---------------------------------------------------------------------------


class Superhostchild(BaseModel):
    """NIOS IPAM superhost child object.

    All 12 swagger properties are present. All non-ref fields are read-only
    (collected in :data:`READONLY_FIELDS`); the resource strips them before
    PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    associated_object: str | None = Field(
        default=None,
        description='The record object, if supported by the WAPI. Otherwise, the value is "None".',
    )
    comment: str | None = Field(default=None, description="The record comment.")
    creation_timestamp: int | None = Field(
        default=None, description="Time at which DNS RR was created."
    )
    data: str | None = Field(default=None, description="Specific data of DNS/DHCP records.")
    disabled: bool | None = Field(
        default=None, description="True if the child DNS/DHCP object is disabled."
    )
    name: str | None = Field(default=None, description="Name of the associated DNS/DHCP object.")
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which this network record resides.",
    )
    parent: str | None = Field(
        default=None, description="Name of the Super Host object in which record resides."
    )
    record_parent: str | None = Field(default=None, description="Name of a parent zone/network.")
    type: (
        Literal[
            "ARecord", "AaaaRecord", "FixedAddress", "HostRecord", "IPv6FixedAddress", "PtrRecord"
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The record type. When searching for an unspecified record type, the search is performed for all records.",
    )  # noqa: A003
    view: str | None = Field(
        default=None, description="Name of the DNS View in which the record resides."
    )
