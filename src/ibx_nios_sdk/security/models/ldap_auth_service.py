# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LdapAuthService - NIOS LDAP authentication service.

All 16 properties from ``components.schemas.LdapAuthService`` in the v2.14
security swagger are represented here. Complex nested fields
``check_ldap_server_settings``, ``ea_mapping``, and ``servers`` are modelled
as ``dict[str, Any] | None`` / ``list[dict[str, Any]] | None`` - see NOTES.md.

WAPI type: ``ldap_auth_service`` (underscore - verified via swagger path).

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class LdapAuthService(BaseModel):
    """NIOS LDAP authentication service.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    check_ldap_server_settings: dict[str, Any] | None = Field(default=None)
    comment: str | None = Field(default=None, description="The LDAP descriptive comment.")
    disable: bool | None = Field(
        default=None, description="Determines if the LDAP authentication service is disabled."
    )
    ea_mapping: list[dict[str, Any]] | None = Field(
        default=None, description="The mapping LDAP fields to extensible attributes."
    )
    ldap_group_attribute: str | None = Field(
        default=None, description="The name of the LDAP attribute that defines group membership."
    )
    ldap_group_authentication_type: Literal["GROUP_ATTRIBUTE", "POSIX_GROUP"] | str | None = Field(
        default=None, description="The LDAP group authentication type."
    )
    ldap_user_attribute: str | None = Field(
        default=None, description="The LDAP userid attribute that is used for search."
    )
    mode: Literal["ORDERED_LIST", "ROUND_ROBIN"] | str | None = Field(
        default=None, description="The LDAP authentication mode."
    )
    name: str | None = Field(default=None, description="The LDAP authentication service name.")
    recovery_interval: int | None = Field(
        default=None,
        description="The period of time in seconds to wait before trying to contact a LDAP server that has been marked as 'DOWN'.",
    )
    retries: int | None = Field(
        default=None, description="The maximum number of LDAP authentication attempts."
    )
    search_scope: Literal["BASE", "ONELEVEL", "SUBTREE"] | str | None = Field(
        default=None, description="The starting point of the LDAP search."
    )
    servers: list[dict[str, Any]] | None = Field(
        default=None, description="The list of LDAP servers used for authentication."
    )
    timeout: int | None = Field(
        default=None, description="The LDAP authentication timeout in seconds."
    )
