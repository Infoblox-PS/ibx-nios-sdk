# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolBlockingpolicy - NIOS parental-control blocking policy."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset({"uuid"})


class ParentalcontrolBlockingpolicy(BaseModel):
    """NIOS parental-control blocking policy."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    name: str | None = Field(default=None, description="The blocking policy name.")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object."
    )  # RO
    value: str | None = Field(default=None, description="The blocking policy value.")
