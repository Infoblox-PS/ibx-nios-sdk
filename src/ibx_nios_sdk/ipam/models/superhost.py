# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Superhost - NIOS IPAM superhost object.

All 9 properties from ``components.schemas.Superhost`` in the v2.14 IPAM
swagger are represented here. Extattrs support is included.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Superhost model
# ---------------------------------------------------------------------------


class Superhost(BaseModel):
    """NIOS IPAM superhost object.

    All 9 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- common ---
    comment: str | None = Field(
        default=None, description="The comment for Super Host."
    )  # --- deletion helper ---
    delete_associated_objects: bool | None = Field(
        default=None,
        description="True if we have to delete all DNS/DHCP associated objects with Super Host, false by default.",
    )  # --- associated objects ---
    dhcp_associated_objects: list[Any] | None = Field(
        default=None,
        description="A list of DHCP objects refs which are associated with Super Host.",
    )
    disabled: bool | None = Field(
        default=None,
        description="Disable all DNS/DHCP associated objects with Super Host if True, False by default.",
    )
    dns_associated_objects: list[Any] | None = Field(
        default=None,
        description="A list of object refs of the DNS resource records which are associated with Super Host.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- identity ---
    name: str | None = Field(
        default=None, description="Name of the Superhost."
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
