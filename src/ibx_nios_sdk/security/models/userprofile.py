# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Userprofile - NIOS user profile (current user).

All 19 properties from ``components.schemas.Userprofile`` in the v2.14 security
swagger are represented here.

This is a read-mostly object representing the current logged-in user's profile.
Most identifying fields are readOnly. PUT is supported for updating preferences.

Operations: GET collection, GET by ref, PUT (no POST/DELETE at WAPI level).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "admin_group",
        "days_to_expire",
        "grid_admin_groups",
        "last_login",
        "name",
        "user_type",
    }
)


class Userprofile(BaseModel):
    """NIOS user profile (current logged-in user).

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    admin_group: str | None = Field(
        default=None,
        description="The Admin Group object to which the admin belongs. An admin user can belong to only one admin group at a time.",
    )
    days_to_expire: int | None = Field(
        default=None, description="The number of days left before the admin's password expires."
    )
    grid_admin_groups: list[str] | None = Field(
        default=None, description="List of Admin Group objects that the current user is mapped to."
    )
    last_login: int | None = Field(
        default=None, description="The timestamp when the admin last logged in."
    )
    name: str | None = Field(default=None, description="The admin name.")
    user_type: Literal["LOCAL", "REMOTE"] | str | None = Field(
        default=None, description="The admin type."
    )  # --- writable ---
    active_dashboard_type: Literal["INFO", "TASK"] | str | None = Field(
        default=None, description="Determines the active dashboard type."
    )
    email: str | None = Field(default=None, description="The email address of the admin.")
    global_search_on_ea: bool | None = Field(
        default=None,
        description="Determines if extensible attribute values will be returned by global search or not.",
    )
    global_search_on_ni_data: bool | None = Field(
        default=None,
        description="Determines if global search will search for network insight devices and interfaces or not.",
    )
    lb_tree_nodes_at_gen_level: int | None = Field(
        default=None, description="Determines how many nodes are displayed at generation levels."
    )
    lb_tree_nodes_at_last_level: int | None = Field(
        default=None, description="Determines how many nodes are displayed at the last level."
    )
    max_count_widgets: int | None = Field(
        default=None,
        description="The maximum count of widgets that can be added to one dashboard.",
    )
    old_password: str | None = Field(
        default=None,
        description="The current password that will be replaced by a new password. To change a password in the database, you must provide both the current and new password values. This is a write-only attribute.",
    )
    password: str | None = Field(
        default=None,
        description="The new password of the admin. To change a password in the database, you must provide both the current and new password values. This is a write-only attribute.",
    )
    table_size: int | None = Field(
        default=None,
        description="The number of lines of data a table or a single list view can contain.",
    )
    time_zone: str | None = Field(default=None, description="The time zone of the admin user.")
    use_time_zone: bool | None = Field(default=None, description="Use flag for: time_zone")
