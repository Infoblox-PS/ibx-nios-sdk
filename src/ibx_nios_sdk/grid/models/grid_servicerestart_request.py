# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartRequest - NIOS Grid service-restart request (all read-only)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "error",
        "forced",
        "group",
        "last_updated_time",
        "member",
        "needed",
        "order",
        "result",
        "service",
        "state",
        "uuid",
    }
)


class GridServicerestartRequest(BaseModel):
    """NIOS Grid service-restart request."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    error: str | None = Field(default=None, description="The error message if restart has failed.")
    forced: bool | None = Field(default=None, description="Indicates if this is a force restart.")
    group: str | None = Field(
        default=None, description="The name of the Restart Group associated with the request."
    )
    last_updated_time: int | None = Field(
        default=None, description="The timestamp when the status of the request has changed."
    )
    member: str | None = Field(default=None, description="The member to restart.")
    needed: Literal["UNKNOWN", "CHECKING", "YES", "NO", "FAILURE"] | str | None = Field(
        default=None, description="Indicates if restart is needed."
    )
    order: int | None = Field(default=None, description="The order to restart.")
    result: Literal["SUCCESS", "TIMEOUT", "FAILURE", "NORESTART"] | str | None = Field(
        default=None, description="The result of the restart operation."
    )
    service: Literal["DNS", "DHCPV4", "DHCPV6"] | str | None = Field(
        default=None, description="The service to restart."
    )
    state: Literal["NEW", "QUEUED", "PROCESSING", "FINISHED"] | str | None = Field(
        default=None, description="The state of the request."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
