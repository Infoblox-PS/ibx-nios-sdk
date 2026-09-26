# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Bulkhostnametemplate - NIOS IPAM bulk host name template object.

All 6 properties from ``components.schemas.Bulkhostnametemplate`` in the
v2.14 IPAM swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "is_grid_default",
        "pre_defined",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Bulkhostnametemplate model
# ---------------------------------------------------------------------------


class Bulkhostnametemplate(BaseModel):
    """NIOS IPAM bulk host name template object.

    All 6 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    is_grid_default: bool | None = Field(
        default=None, description="True if this template is Grid default."
    )
    pre_defined: bool | None = Field(
        default=None, description="True if this is a pre-defined template, False otherwise."
    )  # --- template ---
    template_format: str | None = Field(
        default=None,
        description="The format of bulk host name template. It should follow certain rules (please use Administration Guide as reference).",
    )
    template_name: str | None = Field(
        default=None, description="The name of bulk host name template."
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
