# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmAllgroups - NIOS HSM all groups aggregate (read-mostly).

2 properties from ``components.schemas.HsmAllgroups`` in the v2.14 security
swagger are represented here. The ``groups`` field contains references to
HSM group objects (currently only ``hsm:thaleslunagroup`` per the swagger enum).

This is an aggregate/singleton-style object - it represents the combined view
of all HSM groups configured on the appliance.

Operations: GET collection, GET by ref, PUT (aggregate - POST/DELETE not valid).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset()


class HsmAllgroups(BaseModel):
    """NIOS HSM all groups aggregate.

    No readOnly fields in this schema. ``groups`` is a list of group references.
    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable ---
    groups: list[str] | None = Field(
        default=None, description="The list of HSM groups configured on the appliance."
    )
