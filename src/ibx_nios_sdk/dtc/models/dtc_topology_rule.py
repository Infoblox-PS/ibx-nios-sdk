# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyRule - NIOS DTC topology rule.

Operations: GET collection, GET by ref, PUT (no POST or DELETE).

``destination`` and ``sources`` are arrays of complex structs - modelled as
``list[dict[str, Any]] | None``. See NOTES.md.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "topology",
        "uuid",
        "valid",
    }
)


class DtcTopologyRule(BaseModel):
    """NIOS DTC topology rule."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    topology: str | None = Field(default=None, description="The DTC Topology the rule belongs to.")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid: bool | None = Field(
        default=None,
        description="True if the label in the rule exists in the current Topology DB. Always true for SUBNET rules. Rules with non-existent labels may be configured but will never match.",
    )  # --- writable ---
    dest_type: Literal["POOL", "SERVER"] | str | None = Field(
        default=None, description="The type of the destination for this DTC Topology rule."
    )
    destination: list[dict[str, Any]] | None = Field(
        default=None, description="Set of destinations for this DTC Topology rule."
    )
    return_type: Literal["REGULAR", "NOERR", "NXDOMAIN"] | str | None = Field(
        default=None, description="Type of the DNS response for rule."
    )
    sources: list[dict[str, Any]] | None = Field(
        default=None,
        description="The conditions for matching sources. Should be empty to set rule as default destination.",
    )
