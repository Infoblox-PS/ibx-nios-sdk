# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Sharedrecordgroup - NIOS DNS shared record group container.

All 8 properties from ``components.schemas.Sharedrecordgroup`` in the v2.14
DNS swagger are represented here.
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
# Main Sharedrecordgroup model
# ---------------------------------------------------------------------------


class Sharedrecordgroup(BaseModel):
    """NIOS DNS shared record group container.

    All 8 swagger properties are present.  Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- common fields ---
    comment: str | None = Field(
        default=None, description="The descriptive comment of this shared record group."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- core identity ---
    name: str | None = Field(default=None, description="The name of this shared record group.")
    record_name_policy: str | None = Field(
        default=None, description="The record name policy of this shared record group."
    )
    use_record_name_policy: bool | None = Field(
        default=None, description="Use flag for: record_name_policy"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- zone associations ---
    zone_associations: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of zones associated with this shared record group. Starting from NIOS-9.0.6, this field has been updated to a structure that includes FQDN and DNS view details.",
    )
