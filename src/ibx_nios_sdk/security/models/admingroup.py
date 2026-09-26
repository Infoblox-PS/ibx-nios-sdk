# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Admingroup - NIOS admin group.

All 45 properties from ``components.schemas.Admingroup`` in the v2.14 security
swagger are represented here. Complex nested command-set schemas and lockout/
password-setting schemas are approximated as ``dict[str, Any] | None``.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any, Literal

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


class Admingroup(BaseModel):
    """NIOS admin group.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.

    Complex nested command-set and settings types are modelled as
    ``dict[str, Any] | None`` - see NOTES.md.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    access_method: list[Literal["GUI", "API", "TAXII", "CLOUD_API", "CLI"] | str] | None = Field(
        default=None,
        description="Access methods specify whether an admin group can use the GUI and the API to access the appliance or to send Taxii messages to the appliance. Note that API includes both the Perl API and RESTful API.",
    )
    admin_set_commands: dict[str, Any] | None = Field(default=None)
    admin_show_commands: dict[str, Any] | None = Field(default=None)
    admin_toplevel_commands: dict[str, Any] | None = Field(default=None)
    cloud_set_commands: dict[str, Any] | None = Field(default=None)
    cloud_show_commands: dict[str, Any] | None = Field(default=None)
    comment: str | None = Field(
        default=None, description="Comment for the Admin Group; maximum 256 characters."
    )
    database_set_commands: dict[str, Any] | None = Field(default=None)
    database_show_commands: dict[str, Any] | None = Field(default=None)
    dhcp_set_commands: dict[str, Any] | None = Field(default=None)
    dhcp_show_commands: dict[str, Any] | None = Field(default=None)
    disable: bool | None = Field(
        default=None,
        description="Determines whether the Admin Group is disabled or not. When this is set to False, the Admin Group is enabled.",
    )
    disable_concurrent_login: bool | None = Field(
        default=None, description="Disable concurrent login feature"
    )
    dns_set_commands: dict[str, Any] | None = Field(default=None)
    dns_show_commands: dict[str, Any] | None = Field(default=None)
    dns_toplevel_commands: dict[str, Any] | None = Field(default=None)
    docker_set_commands: dict[str, Any] | None = Field(default=None)
    docker_show_commands: dict[str, Any] | None = Field(default=None)
    email_addresses: list[str] | None = Field(
        default=None, description="The e-mail addresses for the Admin Group."
    )
    enable_restricted_user_access: bool | None = Field(
        default=None,
        description="Determines whether the restrictions will be applied to the admin connector level for users of this Admin Group.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    grid_set_commands: dict[str, Any] | None = Field(default=None)
    grid_show_commands: dict[str, Any] | None = Field(default=None)
    inactivity_lockout_setting: dict[str, Any] | None = Field(default=None)
    licensing_set_commands: dict[str, Any] | None = Field(default=None)
    licensing_show_commands: dict[str, Any] | None = Field(default=None)
    lockout_setting: dict[str, Any] | None = Field(
        default=None, description="Account lockout settings (failed-login limits, lockout window)."
    )
    machine_control_toplevel_commands: dict[str, Any] | None = Field(default=None)
    name: str | None = Field(default=None, description="The name of the Admin Group.")
    networking_set_commands: dict[str, Any] | None = Field(default=None)
    networking_show_commands: dict[str, Any] | None = Field(default=None)
    password_setting: dict[str, Any] | None = Field(
        default=None, description="Password policy settings (length, history, complexity)."
    )
    roles: list[str] | None = Field(
        default=None, description="The names of roles this Admin Group applies to."
    )
    saml_setting: dict[str, Any] | None = Field(default=None)
    security_set_commands: dict[str, Any] | None = Field(default=None)
    security_show_commands: dict[str, Any] | None = Field(default=None)
    superuser: bool | None = Field(
        default=None,
        description="Determines whether this Admin Group is a superuser group. A superuser group can perform all operations on the appliance, and can view and configure all types of data.",
    )
    trouble_shooting_toplevel_commands: dict[str, Any] | None = Field(default=None)
    use_account_inactivity_lockout_enable: bool | None = Field(
        default=None, description="This is the use flag for account inactivity lockout settings."
    )
    use_disable_concurrent_login: bool | None = Field(
        default=None, description="Whether to override grid concurrent login"
    )
    use_lockout_setting: bool | None = Field(
        default=None, description="Whether to override grid sequential lockout setting"
    )
    use_password_setting: bool | None = Field(
        default=None, description="Whether grid password expiry setting should be override."
    )
    user_access: list[dict[str, Any]] | None = Field(
        default=None, description="The access control items for this Admin Group."
    )
