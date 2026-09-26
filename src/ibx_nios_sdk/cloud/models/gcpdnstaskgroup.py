# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Gcpdnstaskgroup - NIOS GCP DNS task group object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "project_id",
        "projects_list",
        "sync_status",
        "uuid",
    }
)


class Gcpdnstaskgroup(BaseModel):
    """NIOS GCP DNS task group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    sync_status: Literal["OK", "SYNC_ERROR", "OFFLINE", "NOT_SYNCING"] | str | None = Field(
        default=None, description="Sync status for this task."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="Comment for the task group; maximum 256 characters."
    )
    consolidate_zones: bool | None = Field(
        default=None, description="Indicates if all zones need to be saved into a single view."
    )
    consolidated_view: str | None = Field(
        default=None, description="Consolidate all zones into one view."
    )
    disabled: bool | None = Field(
        default=None, description="Indicates if the task group is enabled or disabled."
    )
    gcp_project_ids_file_token: str | None = Field(
        default=None, description="The Gcp project IDs file's token."
    )
    grid_member: str | None = Field(
        default=None, description="Grid member configured to run this task group."
    )
    multiple_projects_sync_policy: (
        Literal["NONE", "DISCOVER_PROJECTS", "UPLOAD_PROJECTS"] | str | None
    ) = Field(
        default=None,
        description="Discover all child projects or Upload child project ids to discover.",
    )
    name: str | None = Field(default=None, description="The name of this Gcp DNS sync task group.")
    network_view: str | None = Field(
        default=None, description="The name of the tenant's network view."
    )
    network_view_mapping_policy: Literal["AUTO_CREATE", "DIRECT"] | str | None = Field(
        default=None, description="The network view mapping policy."
    )
    project_id: str | None = Field(
        default=None, description="The Gcp project ID associated with this task group."
    )
    projects_list: list[dict[str, Any] | str] | str | None = Field(
        default=None, description="The Gcp Project IDs list associated with this task."
    )
    sync_child_projects: bool | None = Field(
        default=None, description="Synchronizing child projects is enabled or disabled."
    )
    task_control: object | None = Field(
        default=None,
        description="This function performs action on a task. Current support is for RUN action.",
    )
    task_list: list[object] | None = Field(
        default=None, description="List of Gcp DNS tasks in this group."
    )
