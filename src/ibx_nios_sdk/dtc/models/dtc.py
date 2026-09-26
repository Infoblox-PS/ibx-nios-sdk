# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dtc - NIOS DTC global configuration object.

The ``Dtc`` WAPI type (``dtc``) is a singleton-like global config object.
It supports GET (list) and PUT (update by ref) - no POST or DELETE.

Properties from ``components.schemas.Dtc`` in the v2.14 DTC swagger are all
function-schema references modelled as ``dict[str, Any] | None`` - they
represent function call schemas invoked via POST to sub-paths like
``/dtc/add_certificate``. See NOTES.md.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields - none documented on Dtc itself
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset()


class Dtc(BaseModel):
    """NIOS DTC global configuration object.

    All sub-property fields are function-schema references - modelled as
    ``dict[str, Any] | None``. See NOTES.md for details.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # Function-schema properties (all complex sub-schemas → dict)
    add_certificate: dict[str, Any] | None = Field(default=None)
    dtc_get_object_grid_state: dict[str, Any] | None = Field(default=None)
    dtc_object_disable: dict[str, Any] | None = Field(default=None)
    dtc_object_enable: dict[str, Any] | None = Field(default=None)
    generate_ea_topology_db: dict[str, Any] | None = Field(default=None)
    import_maxminddb: dict[str, Any] | None = Field(default=None)
    query: dict[str, Any] | None = Field(default=None)
