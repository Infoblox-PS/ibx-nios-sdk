# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Vlanrange - NIOS IPAM VLAN range object.

All 12 properties from ``components.schemas.Vlanrange`` in the v2.14 IPAM
swagger are represented here.

NOTE: ``next_available_vlan_id`` is a function schema in the swagger; typed
as ``dict[str, Any] | None`` here.
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
# Main Vlanrange model
# ---------------------------------------------------------------------------


class Vlanrange(BaseModel):
    """NIOS IPAM VLAN range object.

    All 12 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- common ---
    comment: str | None = Field(
        default=None, description="A descriptive comment for this VLAN Range."
    )  # --- range control ---
    delete_vlans: bool | None = Field(
        default=None,
        description="Vlans delete option. Determines whether all child objects should be removed alongside with the VLAN Range or child objects should be assigned to another parental VLAN Range/View. By default child objects are re-parented.",
    )  # --- range ---
    end_vlan_id: int | None = Field(
        default=None, description="End ID for VLAN Range."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- identity ---
    name: str | None = Field(
        default=None, description="Name of the VLAN Range."
    )  # --- function schema (not stored; used for function calls only) ---
    next_available_vlan_id: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the next-available-VLAN-ID operation."
    )  # --- range auto-populate ---
    pre_create_vlan: bool | None = Field(
        default=None,
        description="If set on creation VLAN objects will be created once VLAN Range created.",
    )  # --- range ---
    start_vlan_id: int | None = Field(
        default=None, description="Start ID for VLAN Range."
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- naming ---
    vlan_name_prefix: str | None = Field(
        default=None, description="If set on creation prefix string will be used for VLAN name."
    )  # --- parent view ---
    vlan_view: dict[str, Any] | str | None = Field(
        default=None, description="The VLAN View to which this VLAN Range belongs."
    )
