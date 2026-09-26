# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionProfile - NIOS threat protection profile.

All 12 properties from ``components.schemas.ThreatprotectionProfile`` in the
v2.14 threatprotection swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class ThreatprotectionProfile(BaseModel):
    """NIOS threat protection profile.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.

    ``members`` is an array of member-reference objects; approximated as
    ``list[dict[str, Any]] | None`` - see NOTES.md.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The comment for the Threat Protection profile."
    )
    current_ruleset: str | None = Field(
        default=None, description="The current Threat Protection profile ruleset."
    )
    disable_multiple_dns_tcp_request: bool | None = Field(
        default=None,
        description="Determines if multiple BIND responses via TCP connection are disabled.",
    )
    events_per_second_per_rule: int | None = Field(
        default=None, description="The number of events logged per second per rule."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    members: list[str] | None = Field(
        default=None, description="The list of members that are associated with the profile."
    )
    name: str | None = Field(
        default=None, description="The name of the Threat Protection profile."
    )
    source_member: str | None = Field(
        default=None,
        description="The source member. It can be used only during the create operation for cloning a profile from an existing member.",
    )
    source_profile: str | None = Field(
        default=None,
        description="The source profile. It can be used only during the create operation for cloning a profile from an existing profile.",
    )
    use_current_ruleset: bool | None = Field(
        default=None, description="Use flag for: current_ruleset"
    )
    use_disable_multiple_dns_tcp_request: bool | None = Field(
        default=None, description="Use flag for: disable_multiple_dns_tcp_request"
    )
    use_events_per_second_per_rule: bool | None = Field(
        default=None, description="Use flag for: events_per_second_per_rule"
    )
