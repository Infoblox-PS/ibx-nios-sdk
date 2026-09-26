# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dns64group - NIOS DNS64 group.

All 11 properties from ``components.schemas.Dns64group`` in the v2.14 DNS
swagger are represented here.  Nested objects (clients, exclude, mapped) each
have an ``address`` and ``permission`` field.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import _DnsNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Nested types
# ---------------------------------------------------------------------------


class Dns64groupAddressAcl(_DnsNested):
    """Shared structure for clients, exclude, and mapped ACL entries."""

    address: str | None = Field(default=None, description="The address of the Zone Name Server.")
    permission: Literal["ALLOW", "DENY"] | str | None = Field(
        default=None, description="The permission to use for this address."
    )  # ---------------------------------------------------------------------------


# Main Dns64group model
# ---------------------------------------------------------------------------


class Dns64group(BaseModel):
    """NIOS DNS64 group."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- identity ---
    name: str | None = Field(
        default=None, description="The name of the DNS64 synthesis group object."
    )
    comment: str | None = Field(
        default=None, description="The descriptive comment for the DNS64 synthesis group object."
    )
    disable: bool | None = Field(
        default=None, description="Determines whether the DNS64 synthesis group is disabled."
    )  # --- DNS64 settings ---
    enable_dnssec_dns64: bool | None = Field(
        default=None,
        description="Determines whether the DNS64 synthesis of AAAA records is enabled for DNS64 synthesis groups that request DNSSEC data.",
    )
    prefix: str | None = Field(
        default=None,
        description="The IPv6 prefix used for the synthesized AAAA records. The prefix length must be /32, /40, /48, /56, /64 or /96, and all bits beyond the specified length must be zero.",
    )  # --- ACL lists ---
    clients: list[Dns64groupAddressAcl] | None = Field(
        default=None,
        description="Access Control settings that contain IPv4 and IPv6 DNS clients and networks to which the DNS server is allowed to send synthesized AAAA records with the specified IPv6 prefix.",
    )
    exclude: list[Dns64groupAddressAcl] | None = Field(
        default=None,
        description="Access Control settings that contain IPv6 addresses or prefix ranges that cannot be used by IPv6-only hosts, such as IP addresses in the ::ffff:0:0/96 network. When DNS server retrieves an AAAA record that contains an IPv6 address that matches an excluded address, it does not return the AAAA record. Instead it synthesizes an AAAA record from the A record.",
    )
    mapped: list[Dns64groupAddressAcl] | None = Field(
        default=None,
        description="Access Control settings that contain IPv4 addresses and networks for which the DNS server can synthesize AAAA records with the specified prefix.",
    )  # --- extended attributes ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # RO
