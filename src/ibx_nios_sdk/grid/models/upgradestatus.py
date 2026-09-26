# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Upgradestatus - NIOS upgrade status (read-only)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# Nearly all fields are read-only; we still provide READONLY_FIELDS for the resource layer
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "allow_distribution",
        "allow_distribution_scheduling",
        "allow_upgrade",
        "allow_upgrade_cancel",
        "allow_upgrade_pause",
        "allow_upgrade_resume",
        "allow_upgrade_scheduling",
        "allow_upgrade_test",
        "allow_upload",
        "alternate_version",
        "comment",
        "current_version",
        "current_version_summary",
        "distribution_schedule_active",
        "distribution_schedule_time",
        "distribution_state",
        "distribution_version",
        "distribution_version_summary",
        "element_status",
        "grid_state",
        "group_state",
        "ha_status",
        "hotfixes",
        "ipv4_address",
        "ipv6_address",
        "member",
        "message",
        "pnode_role",
        "reverted",
        "status_time",
        "status_value",
        "status_value_update_time",
        "steps",
        "steps_completed",
        "steps_total",
        "subelement_type",
        "subelements_completed",
        "subelements_total",
        "type",
        "upgrade_group",
        "upgrade_schedule_active",
        "upgrade_state",
        "upgrade_test_status",
        "upload_version",
        "upload_version_summary",
    }
)


class Upgradestatus(BaseModel):
    """NIOS upgrade status (read-only)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    allow_distribution: bool | None = Field(
        default=None, description="Determines if distribution is allowed for the Grid."
    )
    allow_distribution_scheduling: bool | None = Field(
        default=None, description="Determines if distribution scheduling is allowed."
    )
    allow_upgrade: bool | None = Field(
        default=None, description="Determines if upgrade is allowed for the Grid."
    )
    allow_upgrade_cancel: bool | None = Field(
        default=None, description="Determines if the Grid is allowed to cancel an upgrade."
    )
    allow_upgrade_pause: bool | None = Field(
        default=None, description="Determines if the Grid is allowed to pause an upgrade."
    )
    allow_upgrade_resume: bool | None = Field(
        default=None, description="Determines if the Grid is allowed to resume an upgrade."
    )
    allow_upgrade_scheduling: bool | None = Field(
        default=None, description="Determine if the Grid is allowed to schedule an upgrade."
    )
    allow_upgrade_test: bool | None = Field(
        default=None, description="Determines if the Grid is allowed to test an upgrade."
    )
    allow_upload: bool | None = Field(
        default=None, description="Determine if the Grid is allowed to upload a build."
    )
    alternate_version: str | None = Field(default=None, description="The alternative version.")
    comment: str | None = Field(
        default=None,
        description="Comment in readable format for an upgrade group a or virtual node.",
    )
    current_version: str | None = Field(default=None, description="The current version.")
    current_version_summary: str | None = Field(
        default=None,
        description="Current version summary for the 'type' requested. This field can be requested for the Grid, a certain group that has virtual nodes as subelements, or for the overall group status.",
    )
    distribution_schedule_active: bool | None = Field(
        default=None, description="Determines if the distribution schedule is active for the Grid."
    )
    distribution_schedule_time: int | None = Field(
        default=None, description="The Grid master distribution schedule time."
    )
    distribution_state: Literal["NONE", "PROGRESSING", "COMPLETED"] | str | None = Field(
        default=None, description="The current state of distribution process."
    )
    distribution_version: str | None = Field(
        default=None, description="The version that is distributed."
    )
    distribution_version_summary: str | None = Field(
        default=None,
        description="Distribution version summary for the 'type' requested. This field can be requested for the Grid, a certain group that has virtual nodes as subelements, or for the overall group status.",
    )
    element_status: Literal["FAILED", "OFFLINE", "WARNING", "WORKING"] | str | None = Field(
        default=None,
        description="The status of a certain element with regards to the type requested.",
    )
    grid_state: (
        Literal[
            "DISTRIBUTING",
            "DEFAULT",
            "UPGRADING_FAILED",
            "REVERTING_COMPLETE",
            "DISTRIBUTING_COMPLETE",
            "NONE",
            "DISTRIBUTING_ENDED",
            "DOWNGRADING_COMPLETE",
            "UPLOADED",
            "DISTRIBUTING_FAILED",
            "DISTRIBUTING_PAUSED",
            "UPGRADING_PAUSED",
            "DOWNGRADING_FAILED",
            "UPGRADING_COMPLETE",
            "REVERTING",
            "REVERTING_FAILED",
            "UPGRADING",
            "TEST_UPGRADING",
        ]
        | str
        | None
    ) = Field(default=None, description="The state of the Grid.")
    group_state: (
        Literal[
            "GROUP_UPGRADING_COMPLETE",
            "GROUP_DISTRIBUTING_FAILED",
            "GROUP_UPGRADING",
            "GROUP_DISTRIBUTING",
            "GROUP_UPGRADING_WAITING",
            "UPGRADE_STARTED",
            "GROUP_NONE",
            "GROUP_DISTRIBUTING_WAITING",
            "GROUP_DISTRIBUTING_COMPLETE",
        ]
        | str
        | None
    ) = Field(default=None, description="The state of a group.")
    ha_status: Literal["ACTIVE", "PASSIVE", "NOT_CONFIGURED"] | str | None = Field(
        default=None, description="Status of the HA pair."
    )
    hotfixes: list[dict[str, object]] | None = Field(
        default=None, description="The list of hotfixes."
    )
    ipv4_address: str | None = Field(
        default=None, description="The IPv4 Address of virtual node or physical one."
    )
    ipv6_address: str | None = Field(
        default=None, description="The IPv6 Address of virtual node or physical one."
    )
    member: str | None = Field(
        default=None, description="Member that participates in the upgrade process."
    )
    message: str | None = Field(default=None, description="The Grid message.")
    pnode_role: str | None = Field(
        default=None, description="Status of the physical node in the HA pair."
    )
    reverted: bool | None = Field(
        default=None, description="Determines if the upgrade process is reverted."
    )
    status_time: int | None = Field(default=None, description="The status time.")
    status_value: (
        Literal["PROGRESSING", "FAILURE", "COMPLETED", "NO_STATUS", "NOT_CONNECTED"] | str | None
    ) = Field(
        default=None, description="Status of a certain group, virtual node or physical node."
    )
    status_value_update_time: int | None = Field(
        default=None, description="Timestamp of when the status was updated."
    )
    steps: list[dict[str, object]] | None = Field(
        default=None, description="The list of upgrade process steps."
    )
    steps_completed: int | None = Field(default=None, description="The number of steps done.")
    steps_total: int | None = Field(
        default=None, description="Total number steps in the upgrade process."
    )
    subelement_type: Literal["PNODE", "GROUP", "VNODE"] | str | None = Field(
        default=None,
        description="The type of subelements to be requested. If 'type' is 'GROUP', or 'VNODE', then 'upgrade_group' or 'member' should have proper values for an operation to return data specific for the values passed. Otherwise, overall data is returned for every group or physical node.",
    )
    subelements_completed: int | None = Field(
        default=None, description="Number of subelements that have accomplished an upgrade."
    )
    subelements_status: list[dict[str, Any] | str] | None = Field(
        default=None, description="The upgrade process information of subelements."
    )
    subelements_total: int | None = Field(
        default=None,
        description="Number of subelements number in a certain group, virtual node, or the Grid.",
    )
    type: Literal["GRID", "GROUP", "VNODE", "PNODE"] | str | None = Field(
        default=None, description="The type of upper level elements to be requested."
    )
    upgrade_group: str | None = Field(
        default=None, description="Upgrade group that participates in the upgrade process."
    )
    upgrade_schedule_active: bool | None = Field(
        default=None, description="Determines if the upgrade schedule is active."
    )
    upgrade_state: Literal["PROGRESSING", "NONE"] | str | None = Field(
        default=None, description="The upgrade state of the Grid."
    )
    upgrade_test_status: Literal["PROGRESSING", "NONE", "FAILED", "COMPLETED"] | str | None = (
        Field(default=None, description="The upgrade test status of the Grid.")
    )
    upload_version: str | None = Field(default=None, description="The version that is uploaded.")
    upload_version_summary: str | None = Field(
        default=None,
        description="Upload version summary for the 'type' requested. This field can be requested for the Grid, a certain group that has virtual nodes as subelements, or overall group status.",
    )
