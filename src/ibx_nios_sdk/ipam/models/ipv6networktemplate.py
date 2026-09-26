# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6networktemplate - NIOS IPAM IPv6 network template.

All 46 properties from ``components.schemas.Ipv6networktemplate`` in the v2.14
IPAM swagger are represented here. Deeply nested types are typed as
``list[dict[str, Any]] | None`` or ``dict[str, Any] | None``.

NOTE: The following complex nested schemas are inlined as dicts:
  - Ipv6networktemplateDelegatedMember
  - Ipv6networktemplateLogicFilterRules (array items)
  - Ipv6networktemplateMembers (array items)
  - Ipv6networktemplateOptions (array items)
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import DhcpOption, ExtAttrValue, LogicFilterRule

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "rir",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Ipv6networktemplate model
# ---------------------------------------------------------------------------


class Ipv6networktemplate(BaseModel):
    """NIOS IPAM IPv6 network template.

    All 46 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- template settings ---
    allow_any_netmask: bool | None = Field(
        default=None,
        description='This flag controls whether the template allows any netmask. You must specify a netmask when creating a network using this template. If you set this parameter to False, you must specify the "cidr" field for the network template object.',
    )
    auto_create_reversezone: bool | None = Field(
        default=None,
        description="This flag controls whether reverse zones are automatically created when the network is added.",
    )  # --- prefix length ---
    cidr: int | None = Field(
        default=None, description="The CIDR of the network in CIDR format."
    )  # --- cloud API ---
    cloud_api_compatible: bool | None = Field(
        default=None,
        description="This flag controls whether this template can be used to create network objects in a cloud-computing deployment.",
    )  # --- common ---
    comment: str | None = Field(
        default=None, description="Comment for the network; maximum 256 characters."
    )  # --- DDNS ---
    ddns_domainname: str | None = Field(
        default=None,
        description="The dynamic DNS domain name the appliance uses specifically for DDNS updates for this network.",
    )
    ddns_enable_option_fqdn: bool | None = Field(
        default=None,
        description="Use this method to set or retrieve the ddns_enable_option_fqdn flag of a DHCP IPv6 Network object. This method controls whether the FQDN option sent by the client is to be used, or if the server can automatically generate the FQDN. This setting overrides the upper-level settings.",
    )
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server is allowed to update DNS, regardless of the DHCP client requests. Note that changes for this field take effect only if ddns_enable_option_fqdn is True.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DNS update Time to Live (TTL) value of a DHCP network object. The TTL is a 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )  # --- delegated member (complex nested - dict) ---
    delegated_member: dict[str, Any] | None = Field(
        default=None,
        description="The Cloud Platform Appliance to which authority of the object is delegated.",
    )  # --- IPv6 DNS ---
    domain_name: str | None = Field(
        default=None,
        description="Use this method to set or retrieve the domain_name value of a DHCP IPv6 Network object.",
    )
    domain_name_servers: list[str] | None = Field(
        default=None,
        description="Use this method to set or retrieve the dynamic DNS updates flag of a DHCP IPv6 Network object. The DHCP server can send DDNS updates to DNS servers in the same Grid and to external DNS servers. This setting overrides the member level settings.",
    )  # --- DDNS flags ---
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP IPv6 network object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- fixed address templates ---
    fixed_address_templates: list[str] | None = Field(
        default=None,
        description="The list of IPv6 fixed address templates assigned to this IPv6 network template object. When you create an IPv6 network based on an IPv6 network template object that contains IPv6 fixed address templates, the IPv6 fixed addresses are created based on the associated IPv6 fixed address templates.",
    )  # --- IPv6 prefix ---
    ipv6prefix: str | None = Field(
        default=None, description="The IPv6 Address prefix of the DHCP IPv6 network."
    )  # --- logic filters ---
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on this IPv6 network template. This list corresponds to the match rules that are written to the DHCPv6 configuration file.",
    )  # --- members (complex nested - list of dicts) ---
    members: list[dict[str, Any]] | None = Field(
        default=None,
        description='A list of members that serve DHCP for the network. All members in the array must be of the same type. The struct type must be indicated in each element, by setting the "_struct" member to the struct type.',
    )  # --- core identity ---
    name: str | None = Field(
        default=None, description="The name of this IPv6 network template."
    )  # --- DHCP options (complex nested - list of dicts) ---
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )  # --- IPv6 DHCP lifetimes ---
    preferred_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the preferred lifetime value of a DHCP IPv6 Network object.",
    )  # --- range templates ---
    range_templates: list[str] | None = Field(
        default=None,
        description="The list of IPv6 address range templates assigned to this IPv6 network template object. When you create an IPv6 network based on an IPv6 network template object that contains IPv6 range templates, the IPv6 address ranges are created based on the associated IPv6 address range templates.",
    )  # --- lease recycling ---
    recycle_leases: bool | None = Field(
        default=None,
        description="If the field is set to True, the leases are kept in the Recycle Bin until one week after expiration. Otherwise, the leases are permanently deleted.",
    )  # --- read-only ---
    rir: Literal["RIPE", "NONE"] | str | None = Field(
        default=None,
        description="The registry (RIR) that allocated the IPv6 network address space.",
    )  # --- RIR ---
    rir_organization: str | None = Field(
        default=None, description="The RIR organization associated with the IPv6 network."
    )
    rir_registration_action: Literal["NONE", "CREATE"] | str | None = Field(
        default=None, description="The action for the RIR registration."
    )
    rir_registration_status: Literal["REGISTERED", "NOT_REGISTERED"] | str | None = Field(
        default=None, description="The registration status of the IPv6 network in RIR."
    )
    send_rir_request: bool | None = Field(
        default=None, description="Determines whether to send the RIR registration request."
    )  # --- DNS on renewal ---
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )  # --- use flags ---
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_ddns_enable_option_fqdn: bool | None = Field(
        default=None, description="Use flag for: ddns_enable_option_fqdn"
    )
    use_ddns_generate_hostname: bool | None = Field(
        default=None, description="Use flag for: ddns_generate_hostname"
    )
    use_ddns_ttl: bool | None = Field(default=None, description="Use flag for: ddns_ttl")
    use_domain_name: bool | None = Field(default=None, description="Use flag for: domain_name")
    use_domain_name_servers: bool | None = Field(
        default=None, description="Use flag for: domain_name_servers"
    )
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_recycle_leases: bool | None = Field(
        default=None, description="Use flag for: recycle_leases"
    )
    use_update_dns_on_lease_renewal: bool | None = Field(
        default=None, description="Use flag for: update_dns_on_lease_renewal"
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- IPv6 DHCP lifetime ---
    valid_lifetime: int | None = Field(
        default=None,
        description="Use this method to set or retrieve the valid lifetime value of a DHCP IPv6 Network object.",
    )
