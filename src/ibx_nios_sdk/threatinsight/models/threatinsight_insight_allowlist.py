# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightInsightAllowlist - NIOS threat insight insight allowlist.

All 2 non-_ref properties from ``components.schemas.ThreatinsightInsightAllowlist`` in
the v2.14 threatinsight swagger are represented here.

Operations: GET collection, GET by ref only (fully read-only - no POST/PUT/DELETE).

Note: The plan listed ``["name", "fqdn", "type", "comment"]`` as default return fields
and properties, but the swagger schema only contains ``uuid`` (readOnly) and ``version``
(readOnly). This object is a read-only aggregate. Default return fields corrected to
``["version"]``.

WAPI type: ``threatinsight:insight_allowlist`` (with underscore - swagger ground truth).
The plan tentatively listed ``insightallowlist`` but the swagger path and tag use
``insight_allowlist``.
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


class ThreatinsightInsightAllowlist(BaseModel):
    """NIOS threat insight insight allowlist - fully read-only.

    Both non-``_ref`` swagger properties are read-only.
    Read-only fields are collected in :data:`READONLY_FIELDS`.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    version: str | None = Field(default=None, description="Allowlist version string.")
