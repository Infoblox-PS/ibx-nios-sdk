# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartStatus - NIOS Grid service-restart status (all read-only)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "failures",
        "finished",
        "grouped",
        "needed_restart",
        "no_restart",
        "parent",
        "pending",
        "pending_restart",
        "processing",
        "restarting",
        "success",
        "timeouts",
    }
)


class GridServicerestartStatus(BaseModel):
    """NIOS Grid service-restart status."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    failures: int | None = Field(default=None, description="The number of failed requests.")
    finished: int | None = Field(default=None, description="The number of finished requests.")
    grouped: Literal["GRID", "GROUP"] | str | None = Field(
        default=None, description="The type of grouping."
    )
    needed_restart: int | None = Field(
        default=None, description="The number of created yet unprocessed requests for restart."
    )
    no_restart: int | None = Field(
        default=None, description="The number of requests that did not require a restart."
    )
    parent: str | None = Field(
        default=None,
        description="A reference to the grid or grid:servicerestart:group object associated with the request.",
    )
    pending: int | None = Field(
        default=None, description="The number of requests that are pending a restart."
    )
    pending_restart: int | None = Field(
        default=None, description="The number of forced or needed requests pending for restart."
    )
    processing: int | None = Field(
        default=None,
        description="The number of not forced and not needed requests pending for restart.",
    )
    restarting: int | None = Field(
        default=None, description="The number of service restarts for corresponding members."
    )
    success: int | None = Field(
        default=None, description="The number of requests associated with successful restarts."
    )
    timeouts: int | None = Field(default=None, description="The number of timeout requests.")
