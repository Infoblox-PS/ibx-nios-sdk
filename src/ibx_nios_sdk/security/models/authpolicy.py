# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Authpolicy - NIOS authentication policy (singleton).

All 6 properties from ``components.schemas.Authpolicy`` in the v2.14 security
swagger are represented here.

This is a singleton object - only one authpolicy exists per grid. Standard CRUD
methods are available but create/delete calls will fail at the WAPI level.

Operations: GET collection, GET by ref, PUT (singleton - POST/DELETE not valid).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Authpolicy(BaseModel):
    """NIOS authentication policy (singleton).

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    admin_groups: list[str] | None = Field(
        default=None,
        description="List of names of local administration groups that are mapped to remote administration groups.",
    )
    auth_services: list[str] | None = Field(
        default=None,
        description="The array that contains an ordered list of refs to :doc:`localuser:authservice object </objects/localuser.authservice>`, ldap_auth_service object ldap_auth_service, :doc:`radius:authservice object </objects/radius.authservice>`, :doc:`tacacsplus:authservice object </objects/tacacsplus.authservice>`, ad_auth_service object ad_auth_service, :doc:`certificate:authservice object </objects/certificate.authservice>`. :doc:`saml:authservice object </objects/saml.authservice>`,",
    )
    default_group: str | None = Field(
        default=None,
        description="The default admin group that provides authentication in case no valid group is found.",
    )
    usage_type: Literal["FULL", "AUTH_ONLY"] | str | None = Field(
        default=None, description="Remote policies usage."
    )
