# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Fingerprint - NIOS DHCP fingerprint.

All 11 properties from ``components.schemas.Fingerprint`` in the v2.14 DHCP
swagger are represented here.

NOTE: ``type`` is a Python builtin name - aliased to ``type_``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Fingerprint(BaseModel):
    """NIOS DHCP fingerprint."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="Comment for the Fingerprint; maximum 256 characters."
    )
    device_class: str | None = Field(
        default=None, description="A class of DHCP Fingerprint object; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None, description="Determines if the DHCP Fingerprint object is disabled or not."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    ipv6_option_sequence: list[str] | None = Field(
        default=None,
        description="A list (comma separated list) of IPv6 option number sequences of the device or operating system.",
    )
    name: str | None = Field(default=None, description="Name of the DHCP Fingerprint object.")
    option_sequence: list[str] | None = Field(
        default=None,
        description="A list (comma separated list) of IPv4 option number sequences of the device or operating system.",
    )
    type_: Literal["STANDARD", "CUSTOM"] | str | None = Field(
        default=None, alias="type", description="Object type discriminator."
    )
    vendor_id: list[str] | None = Field(
        default=None, description="A list of vendor IDs of the device or operating system."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
