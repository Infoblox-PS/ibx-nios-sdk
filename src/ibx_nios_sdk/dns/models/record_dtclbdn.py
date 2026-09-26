# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDtclbdn - NIOS DTC LBDN DNS record (read-only view)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "disable",
        "last_queried",
        "lbdn",
        "name",
        "pattern",
        "uuid",
        "view",
        "zone",
    }
)


class RecordDtclbdn(BaseModel):
    """NIOS DTC LBDN DNS record - read-only projection of DTC LBDN into DNS."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(default=None, description="Comment for the record.")  # RO
    disable: bool | None = Field(
        default=None, description="Determines if the record is disabled."
    )  # RO
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None, description="Extensible attributes associated with the object."
    )
    last_queried: int | None = Field(
        default=None, description="Time of the last DNS query, Epoch seconds."
    )  # RO
    # Schema says string, but NIOS 9.1 returns the dtc:lbdn object inline.
    lbdn: dict[str, Any] | str | None = Field(
        default=None, description="The DTC LBDN object, inline or as a _ref string."
    )  # RO
    name: str | None = Field(default=None, description="The display name of the DTC LBDN.")  # RO
    pattern: str | None = Field(default=None, description="The LBDN wildcard pattern.")  # RO
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object."
    )  # RO
    view: str | None = Field(default=None, description="The DNS view name.")  # RO
    zone: str | None = Field(default=None, description="The zone name.")  # RO
