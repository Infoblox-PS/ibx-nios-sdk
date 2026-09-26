# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dhcpoptiondefinition - NIOS DHCP option definition.

All 6 properties from ``components.schemas.Dhcpoptiondefinition`` in the v2.14 DHCP
swagger are represented here.

NOTE: ``type`` is a Python builtin name - aliased to ``type_``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Dhcpoptiondefinition(BaseModel):
    """NIOS DHCP option definition."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    code: int | None = Field(
        default=None,
        description="The code of a DHCP option definition object. An option code number is used to identify the DHCP option.",
    )
    name: str | None = Field(
        default=None, description="The name of a DHCP option definition object."
    )
    space: str | None = Field(
        default=None, description="The space of a DHCP option definition object."
    )
    type_: (
        Literal[
            "16-bit signed integer",
            "16-bit unsigned integer",
            "32-bit signed integer",
            "32-bit unsigned integer",
            "64-bit unsigned integer",
            "8-bit signed integer",
            "8-bit unsigned integer",
            "8-bit unsigned integer (1,2,4,8)",
            "array of 16-bit integer",
            "array of 16-bit unsigned integer",
            "array of 32-bit integer",
            "array of 32-bit unsigned integer",
            "array of 64-bit unsigned integer",
            "array of 8-bit integer",
            "array of 8-bit unsigned integer",
            "array of ip-address",
            "array of ip-address pair",
            "array of string",
            "binary",
            "boolean",
            "boolean array of ip-address",
            "boolean-text",
            "domain-list",
            "domain-name",
            "encapsulated",
            "ip-address",
            "string",
            "text",
        ]
        | str
        | None
    ) = Field(default=None, alias="type", description="Object type discriminator.")

    # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
