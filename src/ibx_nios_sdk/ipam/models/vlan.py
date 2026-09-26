# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Vlan - NIOS IPAM VLAN object.

All 13 properties from ``components.schemas.Vlan`` in the v2.14 IPAM
swagger are represented here.

NOTE: ``id`` shadows the Python builtin ``id()`` as an attribute name on
instances; this is intentional and acceptable per the plan (no alias needed).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "assigned_to",
        "status",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Vlan model
# ---------------------------------------------------------------------------


class Vlan(BaseModel):
    """NIOS IPAM VLAN object.

    All 13 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    assigned_to: list[str] | None = Field(
        default=None, description="List of objects VLAN is assigned to."
    )  # --- common ---
    comment: str | None = Field(default=None, description="A descriptive comment for this VLAN.")
    contact: str | None = Field(
        default=None, description="Contact information for person/team managing or using VLAN."
    )
    department: str | None = Field(default=None, description="Department where VLAN is used.")
    description: str | None = Field(
        default=None,
        description="Description for the VLAN object, may be potentially used for longer VLAN names.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- identity ---
    id: int | None = Field(default=None, description="VLAN ID value.")  # noqa: A003 - shadows builtin id(); acceptable per plan
    name: str | None = Field(default=None, description="Name of the VLAN.")
    parent: dict[str, Any] | str | None = Field(
        default=None, description="The VLAN View or VLAN Range to which this VLAN belongs."
    )  # --- state ---
    reserved: bool | None = Field(
        default=None, description="When set VLAN can only be assigned to IPAM object manually."
    )  # --- read-only ---
    status: Literal["UNASSIGNED", "ASSIGNED", "RESERVED"] | str | None = Field(
        default=None, description="Status of VLAN object. Can be Assigned, Unassigned, Reserved."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
