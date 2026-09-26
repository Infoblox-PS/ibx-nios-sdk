# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Namedacl - NIOS named ACL.

All 8 properties from ``components.schemas.Namedacl`` in the v2.14 acl
swagger are represented here.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

Read-only fields: ``exploded_access_list``, ``uuid``.

``validate_acl_items`` maps to ``NamedaclValidateAclItems`` which has no
defined properties in the swagger; it is approximated as
``dict[str, Any] | None`` - see NOTES.md.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.acl.models._shared import _AclNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "exploded_access_list",
        "uuid",
    }
)


class NamedaclAccessList(_AclNested):
    """One entry in a named ACL's access_list (NamedaclAccessList schema)."""

    address: str | None = Field(
        default=None, description='The address this rule applies to or "Any".'
    )
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )
    tsig_key: str | None = Field(
        default=None,
        description="A generated TSIG key. If the external primary server is a NIOS appliance running DNS One 2.x code, this can be set to :2xCOMPAT.",
    )
    tsig_key_alg: Literal["HMAC-MD5", "HMAC-SHA256"] | str | None = Field(
        default=None, description="The TSIG key algorithm."
    )
    tsig_key_name: str | None = Field(
        default=None,
        description="The name of the TSIG key. If 2.x TSIG compatibility is used, this is set to 'tsig_xfer' on retrieval, and ignored on insert or update.",
    )
    use_tsig_key_name: bool | None = Field(default=None, description="Use flag for: tsig_key_name")


class Namedacl(BaseModel):
    """NIOS named ACL.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.

    ``validate_acl_items`` is modelled as ``dict[str, Any] | None`` - see
    NOTES.md.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    exploded_access_list: list[NamedaclAccessList] | None = Field(
        default=None,
        description="The exploded access list for the named ACL. This list displays all the access control entries in a named ACL and its nested named ACLs, if applicable.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    access_list: list[NamedaclAccessList] | None = Field(
        default=None,
        description="The access control list of IPv4/IPv6 addresses, networks, TSIG-based anonymous access controls, and other named ACLs.",
    )
    comment: str | None = Field(
        default=None, description="Comment for the named ACL; maximum 256 characters."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    name: str | None = Field(default=None, description="The name of the named ACL.")
    validate_acl_items: dict[str, Any] | None = Field(default=None)
