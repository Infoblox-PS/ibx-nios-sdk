# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Csvimporttask - NIOS CSV import task object.

Operations: GET collection, GET by ref, PUT (no POST/DELETE).
Function: POST /{ref}/stop - stop an in-progress import.

WAPI type: csvimporttask

NOTES:
- Many fields are read-only (status/progress fields).
- 'stop' is a nested function object; typed as dict[str, Any] | None.
- 'uuid' is read-only.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "admin_name",
        "end_time",
        "file_name",
        "file_size",
        "import_id",
        "lines_failed",
        "lines_processed",
        "lines_warning",
        "separator",
        "start_time",
        "status",
        "uuid",
    }
)


class Csvimporttask(BaseModel):
    """NIOS CSV import task."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    admin_name: str | None = Field(
        default=None, description="The login name of the administrator."
    )
    end_time: int | None = Field(
        default=None, description="The end time of this import operation."
    )
    file_name: str | None = Field(
        default=None, description="The name of the file used for the import operation."
    )
    file_size: int | None = Field(
        default=None, description="The size of the file used for the import operation."
    )
    import_id: int | None = Field(default=None, description="The ID of the current import task.")
    lines_failed: int | None = Field(
        default=None, description="The number of lines that encountered an error."
    )
    lines_processed: int | None = Field(
        default=None, description="The number of lines that have been processed."
    )
    lines_warning: int | None = Field(
        default=None, description="The number of lines that encountered a warning."
    )
    separator: Literal["COMMA", "SEMICOLON", "SPACE", "TAB"] | str | None = Field(
        default=None, description="The separator to be used for the data in the CSV file."
    )
    start_time: int | None = Field(
        default=None, description="The start time of the import operation."
    )
    status: (
        Literal[
            "COMPLETED",
            "FAILED",
            "PENDING",
            "RUNNING",
            "STOPPED",
            "UPLOADED",
            "TEST_COMPLETED",
            "TEST_FAILED",
            "TEST_RUNNING",
            "TEST_STOPPED",
        ]
        | str
        | None
    ) = Field(default=None, description="The status of the import operation")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    action: Literal["START", "SAVE"] | str | None = Field(
        default=None, description="The action to execute."
    )
    on_error: Literal["CONTINUE", "STOP"] | str | None = Field(
        default=None, description="The action to take when an error is encountered."
    )
    operation: Literal["INSERT", "UPDATE", "REPLACE", "DELETE", "CUSTOM"] | str | None = Field(
        default=None, description="The operation to execute."
    )
    stop: dict[str, Any] | None = Field(default=None)
    update_method: Literal["MERGE", "OVERRIDE"] | str | None = Field(
        default=None, description="The update method to be used for the operation."
    )
