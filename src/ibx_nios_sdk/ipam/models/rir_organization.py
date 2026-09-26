# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RirOrganization - NIOS RIR organization registered for SWIP/RWhois."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset({"uuid"})


class RirOrganization(BaseModel):
    """NIOS RIR organization."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None, description="Extensible attributes associated with the object."
    )
    id: str | None = Field(default=None, description="The RIR organization identifier.")
    maintainer: str | None = Field(default=None, description="The RIR organization maintainer.")
    name: str | None = Field(default=None, description="The RIR organization name.")
    password: str | None = Field(
        default=None, description="The password for authentication with the RIR."
    )
    rir: str | None = Field(default=None, description="Reference to the parent RIR.")
    sender_email: str | None = Field(
        default=None, description="Sender e-mail used for communication with the RIR."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object."
    )  # RO
