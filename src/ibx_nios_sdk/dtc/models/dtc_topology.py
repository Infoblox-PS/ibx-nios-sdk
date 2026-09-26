# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopology - NIOS DTC topology object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class DtcTopology(BaseModel):
    """NIOS DTC topology."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None,
        description="The comment for the DTC TOPOLOGY monitor object; maximum 256 characters.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    name: str | None = Field(default=None, description="Display name of the DTC Topology.")
    rules: list[dict[str, Any]] | None = Field(default=None, description="Topology rules.")
