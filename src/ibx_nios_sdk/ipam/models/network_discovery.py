# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkDiscovery - NIOS IPAM network discovery aggregate view.

2 properties from ``components.schemas.NetworkDiscovery`` in the v2.14
IPAM swagger are represented here.

NOTE: This is a read-only aggregate view in practice; WAPI will reject
write attempts. No SDK enforcement - callers are responsible.

NOTE: The swagger only has ``_ref`` and ``clear_discovery_data`` (a function
schema). We add ``address``, ``network_view``, and ``discovered_data`` as
commonly-returned extra fields (``extra="allow"`` captures the rest).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields - all fields are effectively read-only
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset()


# ---------------------------------------------------------------------------
# Main NetworkDiscovery model
# ---------------------------------------------------------------------------


class NetworkDiscovery(BaseModel):
    """NIOS IPAM network discovery object.

    Swagger only declares ``_ref`` and ``clear_discovery_data`` (function
    schema).  Extra fields returned by the API are captured via
    ``extra="allow"``.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- function schema (not stored; used for function calls) ---
    clear_discovery_data: dict[str, Any] | None = Field(default=None)
