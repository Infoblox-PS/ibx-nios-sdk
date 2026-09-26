# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Shared nested-type models used across DNS resources."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class _DnsNested(BaseModel):
    """Base for DNS nested types: permissive, name-aware, no _ref."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ExtServer(_DnsNested):
    """External DNS server reference.

    Corresponds to the ``ZoneAuthExternalPrimaries`` /
    ``ZoneAuthExternalSecondaries`` / ``ZoneauthgridprimaryPreferredPrimaries``
    swagger schemas - all share the same 8-field shape.

    Used by ``ZoneAuth.external_primaries``, ``ZoneAuth.external_secondaries``,
    and ``MemberServer.preferred_primaries``.
    """

    address: str | None = Field(default=None, description="IP address of the external DNS server.")
    name: str | None = Field(default=None, description="Name of the external DNS server.")
    shared_with_ms_parent_delegation: bool | None = Field(
        default=None,
        description="Indicates this server is shared with a Microsoft parent delegation.",
    )
    stealth: bool | None = Field(
        default=None, description="If True, the server is stealth (not listed in NS records)."
    )
    tsig_key: str | None = Field(
        default=None, description="The TSIG key value for authenticated zone transfers."
    )
    tsig_key_alg: str | None = Field(
        default=None, description="The algorithm used for the TSIG key."
    )
    tsig_key_name: str | None = Field(
        default=None, description="The name of the TSIG key for authenticated zone transfers."
    )
    use_tsig_key_name: bool | None = Field(default=None, description="Use flag for: tsig_key_name")


class MemberServer(_DnsNested):
    """NIOS Grid member acting as a DNS server.

    Corresponds to the ``ZoneAuthGridPrimary`` / ``ZoneAuthGridSecondaries``
    swagger schemas (6 fields).  The ``preferred_primaries`` list items use
    the same shape as ``ExtServer``.
    """

    name: str | None = Field(default=None, description="Name of the external DNS server.")
    enable_preferred_primaries: bool | None = Field(
        default=None, description="If True, preferred primaries are enabled for this member."
    )
    grid_replicate: bool | None = Field(
        default=None, description="If True, use grid replication for this member."
    )
    lead: bool | None = Field(
        default=None, description="If True, this member is the lead secondary for zone transfers."
    )
    preferred_primaries: list[ExtServer] | None = Field(
        default=None, description="Ordered list of preferred primary servers for zone transfers."
    )
    stealth: bool | None = Field(
        default=None, description="If True, the server is stealth (not listed in NS records)."
    )


class CloudInfo(_DnsNested):
    """Cloud provider / delegation metadata.

    Union of all ``*CloudInfo`` swagger schemas - every variant has the
    same 8 fields (``RecordACloudInfo``, ``ZoneAuthCloudInfo``,
    ``ViewCloudInfo``, etc.).

    Note: the swagger spells the boolean field ``owned_by_adaptor``
    (not ``owned_by_adapter``).  The ``delegated_member`` field is a
    ``$ref`` to a per-object nested struct; typed as ``Any`` here since
    the shape varies by parent object and the field is read-only in
    practice.
    """

    authority_type: str | None = Field(
        default=None, description="The type of cloud authority for this object."
    )
    delegated_member: Any | None = Field(
        default=None, description="The delegated cloud member for this object."
    )
    delegated_root: str | None = Field(
        default=None, description="The root of the delegated cloud zone."
    )
    delegated_scope: str | None = Field(
        default=None, description="The scope of the cloud delegation."
    )
    mgmt_platform: str | None = Field(
        default=None, description="The cloud management platform associated with this object."
    )
    owned_by_adaptor: bool | None = Field(
        default=None, description="If True, this object is owned by the cloud adaptor."
    )
    tenant: str | None = Field(
        default=None, description="The cloud tenant associated with this object."
    )
    usage: str | None = Field(default=None, description="The usage type for the cloud delegation.")
