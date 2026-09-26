# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupForwardingmember - NIOS DNS forwarding-member name-server group.

All 6 properties from ``components.schemas.NsgroupForwardingmember`` in the
v2.14 DNS swagger are represented here.

``forwarding_servers`` entries have a unique 4-field shape (name,
forwarders_only, forward_to list, use_override_forwarders) so an inline nested
type is defined here.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import ExtServer, _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Inline nested type
# ---------------------------------------------------------------------------


class NsgroupForwardingmemberForwardingServer(_DnsNested):
    """A forwarding-member server entry within a forwarding-member NS group."""

    name: str | None = Field(
        default=None, description="The name of the Forwarding Member Name Server Group."
    )
    forwarders_only: bool | None = Field(
        default=None,
        description="Determines if the appliance sends queries to forwarders only, and not to other internal or Internet root servers.",
    )
    forward_to: list[ExtServer] | None = Field(
        default=None,
        description="The information for the remote name servers to which you want the Infoblox appliance to forward queries for a specified domain name.",
    )
    use_override_forwarders: bool | None = Field(
        default=None, description="Use flag for: forward_to"
    )  # ---------------------------------------------------------------------------


# Main NsgroupForwardingmember model
# ---------------------------------------------------------------------------


class NsgroupForwardingmember(BaseModel):
    """NIOS DNS forwarding-member name-server group configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- core identity ---
    name: str | None = Field(
        default=None, description="The name of the Forwarding Member Name Server Group."
    )
    comment: str | None = Field(
        default=None,
        description="Comment for the Forwarding Member Name Server Group; maximum 256 characters.",
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- forwarding servers ---
    forwarding_servers: list[NsgroupForwardingmemberForwardingServer] | None = Field(
        default=None, description="The list of forwarding member servers."
    )  # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
