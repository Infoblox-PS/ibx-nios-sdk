# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Memberdfp - NIOS member DFP (DNS Forwarding Proxy) settings."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset({"host_name", "uuid"})


class Memberdfp(BaseModel):
    """NIOS member DFP settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    dfp_forward_first: bool | None = Field(
        default=None,
        description="Option to resolve DNS query if resolution over Active Trust Cloud failed.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # read-only
    host_name: str | None = Field(default=None, description="Host name of the parent Member")
    is_dfp_override: bool | None = Field(
        default=None, description="DFP override lock'."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
