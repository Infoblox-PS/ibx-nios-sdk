# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcObject - NIOS DTC object (aggregate read view).

Operations: GET collection, GET by ref, PUT (no POST or DELETE).

Almost all fields are read-only; only ``extattrs`` is writable.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "abstract_type",
        "comment",
        "display_type",
        "ipv4_address_list",
        "ipv6_address_list",
        "name",
        "object",
        "status",
        "status_time",
    }
)


class DtcObject(BaseModel):
    """NIOS DTC object - mostly read-only aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    abstract_type: str | None = Field(default=None, description="The abstract object type.")
    comment: str | None = Field(
        default=None, description="The comment for the DTC object; maximum 256 characters."
    )
    display_type: str | None = Field(default=None, description="The display object type.")
    ipv4_address_list: list[str] | None = Field(
        default=None, description="The list of IPv4 addresses."
    )
    ipv6_address_list: list[str] | None = Field(
        default=None, description="The list of IPv6 addresses."
    )
    name: str | None = Field(default=None, description="The display name of the DTC object.")
    object: dict[str, Any] | str | None = Field(
        default=None, description="The specific DTC object."
    )
    status: Literal["NONE", "GREEN", "YELLOW", "RED", "BLUE", "GRAY"] | str | None = Field(
        default=None, description="The availability color status."
    )
    status_time: int | None = Field(
        default=None, description="The timestamp when status or health was last determined."
    )  # --- writable ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
