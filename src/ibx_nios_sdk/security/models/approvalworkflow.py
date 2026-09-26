# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Approvalworkflow - NIOS approval workflow.

All 22 properties from ``components.schemas.Approvalworkflow`` in the v2.14
security swagger are represented here.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Approvalworkflow(BaseModel):
    """NIOS approval workflow.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    approval_group: str | None = Field(
        default=None, description="The approval administration group."
    )
    approval_notify_to: Literal["SUBMITTER", "APPROVER", "BOTH"] | str | None = Field(
        default=None, description="The destination for approval task notifications."
    )
    approved_notify_to: Literal["SUBMITTER", "APPROVER", "BOTH"] | str | None = Field(
        default=None, description="The destination for approved task notifications."
    )
    approver_comment: Literal["UNUSED", "OPTIONAL", "REQUIRED"] | str | None = Field(
        default=None,
        description="The requirement for the comment when an approver approves a submitted task.",
    )
    enable_approval_notify: bool | None = Field(
        default=None, description="Determines whether approval task notifications are enabled."
    )
    enable_approved_notify: bool | None = Field(
        default=None, description="Determines whether approved task notifications are enabled."
    )
    enable_failed_notify: bool | None = Field(
        default=None, description="Determines whether failed task notifications are enabled."
    )
    enable_notify_group: bool | None = Field(
        default=None,
        description="Determines whether e-mail notifications to admin group's e-mail address are enabled.",
    )
    enable_notify_user: bool | None = Field(
        default=None,
        description="Determines whether e-mail notifications to an admin member's e-mail address are enabled.",
    )
    enable_rejected_notify: bool | None = Field(
        default=None, description="Determines whether rejected task notifications are enabled."
    )
    enable_rescheduled_notify: bool | None = Field(
        default=None, description="Determines whether rescheduled task notifications are enabled."
    )
    enable_succeeded_notify: bool | None = Field(
        default=None, description="Determines whether succeeded task notifications are enabled."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    failed_notify_to: Literal["SUBMITTER", "APPROVER", "BOTH"] | str | None = Field(
        default=None, description="The destination for failed task notifications."
    )
    rejected_notify_to: Literal["SUBMITTER", "APPROVER", "BOTH"] | str | None = Field(
        default=None, description="The destination for rejected task notifications."
    )
    rescheduled_notify_to: Literal["SUBMITTER", "APPROVER", "BOTH"] | str | None = Field(
        default=None, description="The destination for rescheduled task notifications."
    )
    submitter_comment: Literal["UNUSED", "OPTIONAL", "REQUIRED"] | str | None = Field(
        default=None,
        description="The requirement for the comment when a submitter submits a task for approval.",
    )
    submitter_group: str | None = Field(
        default=None, description="The submitter administration group."
    )
    succeeded_notify_to: Literal["SUBMITTER", "APPROVER", "BOTH"] | str | None = Field(
        default=None, description="The destination for succeeded task notifications."
    )
    ticket_number: Literal["UNUSED", "OPTIONAL", "REQUIRED"] | str | None = Field(
        default=None,
        description="The requirement for the ticket number when a submitter submits a task for approval.",
    )
