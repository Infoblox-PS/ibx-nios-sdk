# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Fixedaddresstemplate - NIOS DHCP IPv4 fixed address template.

All 29 properties from ``components.schemas.Fixedaddresstemplate`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue, LogicFilterRule

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Fixedaddresstemplate(BaseModel):
    """NIOS DHCP IPv4 fixed address template."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    bootfile: str | None = Field(
        default=None,
        description="The boot file name for the fixed address. You can configure the DHCP server to support clients that use the boot file name option in their DHCPREQUEST messages.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The boot server address for the fixed address. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
    )
    comment: str | None = Field(
        default=None, description="A descriptive comment of a fixed address template object."
    )
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this fixed address.",
    )
    ddns_hostname: str | None = Field(
        default=None, description="The DDNS host name for this fixed address."
    )
    deny_bootp: bool | None = Field(
        default=None,
        description="Determines if BOOTP settings are disabled and BOOTP requests will be denied.",
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="Determines if the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="If this field is set to False, the appliance returns all DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on this fixed address. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )
    name: str | None = Field(
        default=None, description="The name of a fixed address template object."
    )
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address format of the next server that the host needs to boot.",
    )
    number_of_addresses: int | None = Field(
        default=None, description="The number of addresses for this fixed address."
    )
    offset: int | None = Field(
        default=None, description="The start address offset for this fixed address."
    )
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value for a DHCP Fixed Address object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_deny_bootp: bool | None = Field(default=None, description="Use flag for: deny_bootp")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_nextserver: bool | None = Field(default=None, description="Use flag for: nextserver")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_pxe_lease_time: bool | None = Field(
        default=None, description="Use flag for: pxe_lease_time"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
