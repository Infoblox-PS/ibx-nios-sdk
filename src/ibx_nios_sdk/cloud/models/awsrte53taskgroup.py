# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Awsrte53taskgroup - NIOS AWS Route53 task group object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "account_id",
        "accounts_list",
        "sync_status",
        "uuid",
    }
)


class Awsrte53taskgroup(BaseModel):
    """NIOS AWS Route53 task group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    sync_status: Literal["NEW", "OK", "WARNING", "ERROR"] | str | None = Field(
        default=None, description="Indicate the overall sync status of this task group."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    account_id: str | None = Field(
        default=None, description="The AWS Account ID associated with this task group."
    )
    accounts_list: list[dict[str, Any] | str] | str | None = Field(
        default=None, description="The AWS Account IDs list associated with this task group."
    )
    aws_account_ids_file_token: str | None = Field(
        default=None, description="The AWS account IDs file's token."
    )
    comment: str | None = Field(
        default=None, description="Comment for the task group; maximum 256 characters."
    )
    consolidate_zones: bool | None = Field(
        default=None, description="Indicates if all zones need to be saved into a single view."
    )
    consolidated_view: str | None = Field(
        default=None, description="The name of the DNS view for consolidating zones."
    )
    disabled: bool | None = Field(
        default=None, description="Indicates if the task group is enabled or disabled."
    )
    grid_member: str | None = Field(
        default=None, description="Member on which the tasks in this task group will be run."
    )
    multiple_accounts_sync_policy: (
        Literal["NONE", "DISCOVER_CHILDREN", "UPLOAD_CHILDREN"] | str | None
    ) = Field(
        default=None,
        description="Discover all child accounts or Upload child account ids to discover..",
    )
    name: str | None = Field(
        default=None, description="The name of this AWS Route53 sync task group."
    )
    network_view: str | None = Field(
        default=None, description="The name of the tenant's network view."
    )
    network_view_mapping_policy: Literal["AUTO_CREATE", "DIRECT"] | str | None = Field(
        default=None, description="The network view mapping policy."
    )
    role_arn: str | None = Field(
        default=None, description="Role ARN for syncing child accounts; maximum 128 characters."
    )
    sync_child_accounts: bool | None = Field(
        default=None, description="Synchronizing child accounts is enabled or disabled."
    )
    task_control: object | None = Field(
        default=None,
        description="This function performs action on a task. Current support is for RUN action.",
    )
    task_list: list[object] | None = Field(
        default=None, description="List of AWS Route53 tasks in this group."
    )
