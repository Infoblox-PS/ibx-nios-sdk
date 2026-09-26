# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Membercloudsync - NIOS member cloud sync settings."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset({"host_name", "uuid"})


class Membercloudsync(BaseModel):
    """NIOS member cloud sync settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    cloud_sync_enabled: bool | None = Field(
        default=None, description="Option to enable/disable Cloud Sync."
    )  # read-only
    host_name: str | None = Field(
        default=None, description="Host name of the parent Member"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
