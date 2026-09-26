# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Restartservicestatus - NIOS restart service status (read-only)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "dhcp_status",
        "dns_status",
        "member",
        "reporting_status",
        "uuid",
    }
)


class Restartservicestatus(BaseModel):
    """NIOS restart service status (read-only)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    dhcp_status: (
        Literal[
            "CONFIG_ERROR",
            "DISABLED",
            "NO",
            "NO_PERMISSION",
            "NO_REQUEST",
            "OFFLINE",
            "REQUESTING",
            "RESTART_PENDING",
            "YES",
        ]
        | str
        | None
    ) = Field(default=None, description="The status of the DHCP service.")  # read-only
    dns_status: (
        Literal[
            "CONFIG_ERROR",
            "DISABLED",
            "NO",
            "NO_PERMISSION",
            "NO_REQUEST",
            "OFFLINE",
            "REQUESTING",
            "RESTART_PENDING",
            "YES",
        ]
        | str
        | None
    ) = Field(default=None, description="The status of the DNS service.")  # read-only
    member: str | None = Field(
        default=None, description="The name of this Grid member in FQDN format."
    )  # read-only
    reporting_status: (
        Literal[
            "CONFIG_ERROR",
            "DISABLED",
            "NO",
            "NO_PERMISSION",
            "NO_REQUEST",
            "OFFLINE",
            "REQUESTING",
            "RESTART_PENDING",
            "YES",
        ]
        | str
        | None
    ) = Field(default=None, description="The status of the reporting service.")  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
