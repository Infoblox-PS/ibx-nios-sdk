# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverAdsitesSite - NIOS MS server AD sites site.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
Also has a function sub-path move_subnets (POST).

NOTE: move_subnets → dict[str, Any] | None.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset()


class MsserverAdsitesSite(BaseModel):
    """NIOS MS server AD sites site."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable ---
    domain: str | None = Field(
        default=None,
        description="The reference to the Active Directory Domain to which the site belongs.",
    )
    move_subnets: dict[str, Any] | None = Field(default=None)
    name: str | None = Field(
        default=None,
        description="The name of the site properties object for the Active Directory Sites.",
    )
    networks: list[str] | None = Field(
        default=None, description="The list of networks to which the device interfaces belong."
    )
