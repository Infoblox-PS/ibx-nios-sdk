# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Filterfingerprint - NIOS DHCP fingerprint filter."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Filterfingerprint(BaseModel):
    """NIOS DHCP fingerprint filter."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(default=None, description="The descriptive comment.")
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    fingerprint: list[str] | None = Field(
        default=None, description="The list of DHCP Fingerprint objects."
    )
    name: str | None = Field(
        default=None, description="The name of a DHCP Fingerprint Filter object."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
