# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightCloudclient - NIOS threat insight cloud client configuration.

All 5 non-_ref properties from ``components.schemas.ThreatinsightCloudclient`` in the
v2.14 threatinsight swagger are represented here.

Operations: GET collection, GET by ref, PUT (no POST/DELETE - singleton-style).

Note: The plan listed ``["enable", "host", "last_synced"]`` as default return fields but
neither ``host`` nor ``last_synced`` exist in the swagger schema. Default return fields
are corrected to ``["enable"]``.

``force_refresh`` is writeOnly in swagger - present in PUT body but never in GET responses.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class ThreatinsightCloudclient(BaseModel):
    """NIOS threat insight cloud client configuration.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT.

    ``force_refresh`` is writeOnly - it triggers a refresh when included in a PUT
    body but is never returned in GET responses.

    ``blacklist_rpz_list`` is an array of RPZ zone reference strings.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    blacklist_rpz_list: list[str] | None = Field(
        default=None,
        description="The RPZs to which you apply newly detected domains through the Infoblox Threat Insight Cloud Client.",
    )
    enable: bool | None = Field(
        default=None,
        description="Determines whether the Threat Insight in Cloud Client is enabled.",
    )
    force_refresh: bool | None = Field(
        default=None, description="Force a refresh if at least one RPZ is configured."
    )
    interval: int | None = Field(
        default=None,
        description="The time interval (in seconds) for requesting newly detected domains by the Infoblox Threat Insight Cloud Client and applying them to the list of configured RPZs.",
    )
