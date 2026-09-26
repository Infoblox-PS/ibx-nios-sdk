# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberThreatinsight - NIOS member threat insight settings (mostly read-only)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "host_name",
        "ipv4_address",
        "ipv6_address",
        "status",
        "uuid",
    }
)


class MemberThreatinsight(BaseModel):
    """NIOS member threat insight settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    comment: str | None = Field(default=None, description="The Grid member descriptive comment.")
    enable_service: bool | None = Field(
        default=None, description="Determines whether the threat insight service is enabled."
    )  # read-only
    host_name: str | None = Field(
        default=None, description="The Grid member host name."
    )  # read-only
    ipv4_address: str | None = Field(
        default=None, description="The IPv4 Address address of the Grid member."
    )  # read-only
    ipv6_address: str | None = Field(
        default=None, description="The IPv6 Address address of the Grid member."
    )  # read-only
    status: Literal["UNKNOWN", "INACTIVE", "WORKING", "WARNING", "FAILED"] | str | None = Field(
        default=None, description="The Grid member threat insight status."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
