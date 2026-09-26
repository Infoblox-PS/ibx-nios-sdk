# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Rir - NIOS Regional Internet Registry (RIR) configuration."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset({"uuid"})


class Rir(BaseModel):
    """NIOS Regional Internet Registry (RIR) configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    communication_mode: Literal["EMAIL", "API", "NONE"] | str | None = Field(
        default=None, description="The communication mode for the RIR."
    )
    email: str | None = Field(default=None, description="The RIR e-mail address.")
    name: Literal["RIPE"] | str | None = Field(default=None, description="The RIR name.")
    url: str | None = Field(default=None, description="The RIR URL.")
    use_email: bool | None = Field(default=None, description="Use flag for: email")
    use_url: bool | None = Field(default=None, description="Use flag for: url")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object."
    )  # RO
