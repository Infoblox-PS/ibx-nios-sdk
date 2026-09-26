# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Adminuser - NIOS admin user.

All 19 properties from ``components.schemas.Adminuser`` in the v2.14 security
swagger are represented here. ``ssh_keys`` is an array of nested SSH key
objects, modelled as ``list[dict[str, Any]] | None`` - see NOTES.md.

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
        "status",
        "uuid",
    }
)


class Adminuser(BaseModel):
    """NIOS admin user.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    status: Literal["ACTIVE", "INACTIVE", "LOCKED", "DISABLED"] | str | None = Field(
        default=None, description="Status of the user account."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    admin_groups: list[str] | None = Field(
        default=None,
        description="The names of the Admin Groups to which this Admin User belongs. Currently, this is limited to only one Admin Group.",
    )
    auth_method: Literal["KEYPAIR", "KEYPAIR_PASSWORD"] | str | None = Field(
        default=None, description="Determines the way of authentication"
    )
    auth_type: Literal["LOCAL", "RADIUS", "REMOTE", "SAML", "SAML_LOCAL"] | str | None = Field(
        default=None, description="The authentication type for the admin user."
    )
    ca_certificate_issuer: str | None = Field(
        default=None,
        description="The CA certificate that is used for user lookup during authentication.",
    )
    client_certificate_serial_number: str | None = Field(
        default=None, description="The serial number of the client certificate."
    )
    comment: str | None = Field(
        default=None, description="Comment for the admin user; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether the admin user is disabled or not. When this is set to False, the admin user is enabled.",
    )
    email: str | None = Field(default=None, description="The e-mail address for the admin user.")
    enable_certificate_authentication: bool | None = Field(
        default=None,
        description="Determines whether the user is allowed to log in only with the certificate. Regular username/password authentication will be disabled for this user.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    name: str | None = Field(default=None, description="The name of the admin user.")
    password: str | None = Field(
        default=None, description="The password for the administrator to use when logging in."
    )
    ssh_keys: list[dict[str, Any]] | None = Field(
        default=None, description="List of ssh keys for a particular user."
    )
    time_zone: str | None = Field(default=None, description="The time zone for this admin user.")
    use_ssh_keys: bool | None = Field(
        default=None, description="\\, Enable/disable the ssh keypair authentication."
    )
    use_time_zone: bool | None = Field(default=None, description="Use flag for: time_zone")
