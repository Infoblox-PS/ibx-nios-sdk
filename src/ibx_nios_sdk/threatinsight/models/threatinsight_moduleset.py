# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightModuleset - NIOS threat insight module set.

All 2 non-_ref properties from ``components.schemas.ThreatinsightModuleset`` in
the v2.14 threatinsight swagger are represented here.

Operations: GET collection, GET by ref only (fully read-only - no POST/PUT/DELETE).

Note: The plan listed ``["version", "last_updated"]`` as default return fields but
``last_updated`` does not exist in the swagger schema. Default return fields corrected
to ``["version"]``.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - all non-_ref fields
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
        "version",
    }
)


class ThreatinsightModuleset(BaseModel):
    """NIOS threat insight module set - fully read-only.

    Both non-``_ref`` swagger properties are read-only.
    Read-only fields are collected in :data:`READONLY_FIELDS`.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    version: str | None = Field(
        default=None, description="The version number of the threat insight module set."
    )
