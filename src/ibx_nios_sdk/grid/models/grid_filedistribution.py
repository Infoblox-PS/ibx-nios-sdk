# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridFiledistribution - NIOS Grid file distribution settings.

All properties from ``components.schemas.GridFiledistribution`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "current_usage",
        "global_status",
        "name",
        "uuid",
    }
)


class GridFiledistribution(BaseModel):
    """NIOS Grid file distribution settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allow_uploads: bool | None = Field(
        default=None, description="Determines whether the uploads to Grid members are allowed."
    )
    backup_storage: bool | None = Field(
        default=None, description="Determines whether to include distributed files in the backup."
    )  # read-only
    current_usage: int | None = Field(
        default=None,
        description="The value is the percentage of the allocated TFTP storage space that is used, expressed in tenth of a percent. Valid values are from 0 to 1000.",
    )
    enable_anonymous_ftp: bool | None = Field(
        default=None, description="Determines whether the FTP anonymous login is enabled."
    )  # read-only
    global_status: Literal["UNKNOWN", "INACTIVE", "WORKING", "WARNING", "FAILED"] | str | None = (
        Field(default=None, description="The Grid file distribution global status.")
    )  # read-only
    name: str | None = Field(default=None, description="The Grid name.")
    storage_limit: int | None = Field(
        default=None,
        description="Maximum storage in megabytes allowed on the Grid. The maximum storage space allowed for all file distribution services on a Grid is equal to the storage space allowed to the Grid member with the smallest amount of space allowed.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
