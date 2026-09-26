# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartGroup - NIOS Grid service-restart group."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "is_default",
        "last_updated_time",
        "position",
        "requests",
        "status",
        "uuid",
    }
)


class GridServicerestartGroup(BaseModel):
    """NIOS Grid service-restart group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="Comment for the Restart Group; maximum 256 characters."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # read-only
    is_default: bool | None = Field(
        default=None, description="Determines if this Restart Group is the default group."
    )  # read-only
    last_updated_time: int | None = Field(
        default=None,
        description="The timestamp when the status of the latest request has changed.",
    )
    members: list[str] | None = Field(
        default=None, description="The list of members belonging to the group."
    )
    mode: Literal["SEQUENTIAL", "SIMULTANEOUS"] | str | None = Field(
        default=None, description="The default restart method for this Restart Group."
    )
    name: str | None = Field(
        default=None, description="The name of this Restart Group."
    )  # read-only
    position: int | None = Field(default=None, description="The order to restart.")
    recurring_schedule: dict[str, Any] | None = Field(default=None)  # read-only
    requests: list[str] | None = Field(
        default=None, description="The list of requests associated with a restart group."
    )
    service: Literal["DHCP", "DNS"] | str | None = Field(
        default=None, description="The applicable service for this Restart Group."
    )  # read-only
    status: dict[str, Any] | str | None = Field(
        default=None, description="The restart status for a restart group."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
