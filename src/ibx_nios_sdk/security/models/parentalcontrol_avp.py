# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolAvp - NIOS parental-control AVP (RADIUS attribute/value pair)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset({"user_defined", "uuid"})


class ParentalcontrolAvp(BaseModel):
    """NIOS parental-control attribute-value-pair definition."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(default=None, description="Comment for the AVP.")
    domain_types: (
        list[Literal["SUBS_ID", "ANCILLARY", "NAS_CONTEXT", "IP_SPACE_DIS"] | str] | None
    ) = Field(default=None, description="Domain types that this AVP applies to.")
    is_restricted: bool | None = Field(
        default=None, description="Indicates whether the AVP is restricted."
    )
    name: str | None = Field(default=None, description="The AVP name.")
    type: int | None = Field(default=None, description="The AVP RADIUS attribute type.")
    user_defined: bool | None = Field(
        default=None, description="Indicates whether the AVP is user-defined."
    )  # RO
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object."
    )  # RO
    value_type: (
        Literal[
            "IPV6ADDR",
            "STRING",
            "DATE",
            "INTEGER",
            "BYTE",
            "IPV6IFID",
            "IPADDR",
            "SHORT",
            "IPV6PREFIX",
            "OCTETS",
            "INTEGER64",
        ]
        | str
        | None
    ) = Field(default=None, description="The AVP value type.")
    vendor_id: int | None = Field(default=None, description="The RADIUS vendor-id.")
    vendor_type: int | None = Field(default=None, description="The RADIUS vendor-type.")
