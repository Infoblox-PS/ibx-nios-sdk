# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Networktemplate - NIOS IPAM network template.

All 72 properties from ``components.schemas.Networktemplate`` in the v2.14
IPAM swagger are represented here. Deeply nested types are typed as
``list[dict[str, Any]] | None`` or ``dict[str, Any] | None``.

NOTE: The following complex nested schemas are inlined as dicts:
  - NetworktemplateDelegatedMember
  - NetworktemplateIpamThresholdSettings
  - NetworktemplateIpamTrapSettings
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
# Main Networktemplate model
# ---------------------------------------------------------------------------


class Networktemplate(BaseModel):
    """NIOS IPAM network template.

    All 72 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- template settings ---
    allow_any_netmask: bool | None = Field(
        default=None,
        description='This flag controls whether the template allows any netmask. You must specify a netmask when creating a network using this template. If you set this parameter to false, you must specify the "netmask" field for the network template object.',
    )
    authority: bool | None = Field(default=None, description="Authority for the DHCP network.")
    auto_create_reversezone: bool | None = Field(
        default=None,
        description="This flag controls whether reverse zones are automatically created when the network is added.",
    )  # --- BOOTP ---
    bootfile: str | None = Field(
        default=None,
        description="The boot server IPv4 Address or name in FQDN format for the network. You can specify the name and/or IP address of the boot server that the host needs to boot.",
    )
    bootserver: str | None = Field(
        default=None,
        description="The bootserver address for the network. You can specify the name and/or IP address of the boot server that the host needs to boot. The boot server IPv4 Address or name in FQDN format.",
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
    ddns_generate_hostname: bool | None = Field(
        default=None,
        description="If this field is set to True, the DHCP server generates a hostname and updates DNS with it when the DHCP client request does not contain a hostname.",
    )
    ddns_server_always_updates: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server is allowed to update DNS, regardless of the DHCP client requests. Note that changes for this field take effect only if ddns_use_option81 is True.",
    )
    ddns_ttl: int | None = Field(
        default=None,
        description="The DNS update Time to Live (TTL) value of a DHCP network object. The TTL is a 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )
    ddns_update_fixed_addresses: bool | None = Field(
        default=None,
        description="By default, the DHCP server does not update DNS when it allocates a fixed address to a client. You can configure the DHCP server to update the A and PTR records of a client with a fixed address. When this feature is enabled and the DHCP server adds A and PTR records for a fixed address, the DHCP server never discards the records.",
    )
    ddns_use_option81: bool | None = Field(
        default=None, description="The support for DHCP Option 81 at the network level."
    )  # --- delegated member (complex nested - dict) ---
    delegated_member: dict[str, Any] | None = Field(
        default=None,
        description="The Cloud Platform Appliance to which authority of the object is delegated.",
    )  # --- DHCP ---
    deny_bootp: bool | None = Field(
        default=None,
        description="If set to True, BOOTP settings are disabled and BOOTP requests will be denied.",
    )  # --- email ---
    email_list: list[str] | None = Field(
        default=None,
        description="The e-mail lists to which the appliance sends DHCP threshold alarm e-mail messages.",
    )  # --- DDNS flags ---
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP network object. If set to True, the DHCP server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_dhcp_thresholds: bool | None = Field(
        default=None, description="Determines if DHCP thresholds are enabled for the network."
    )
    enable_email_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are sent through email."
    )
    enable_pxe_lease_time: bool | None = Field(
        default=None,
        description="Set this to True if you want the DHCP server to use a different lease time for PXE clients.",
    )
    enable_snmp_warnings: bool | None = Field(
        default=None, description="Determines if DHCP threshold warnings are send through SNMP."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- fixed address templates ---
    fixed_address_templates: list[str] | None = Field(
        default=None,
        description="The list of fixed address templates assigned to this network template object. When you create a network based on a network template object that contains fixed address templates, the fixed addresses are created based on the associated fixed address templates.",
    )  # --- thresholds ---
    high_water_mark: int | None = Field(
        default=None,
        description="The percentage of DHCP network usage threshold above which network usage is not expected and may warrant your attention. When the high watermark is reached, the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    high_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage of DHCP network usage below which the corresponding SNMP trap is reset. A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The high watermark reset value must be lower than the high watermark value.",
    )  # --- DHCP options ---
    ignore_dhcp_option_list_request: bool | None = Field(
        default=None,
        description="If this field is set to False, the appliance returns all DHCP options the client is eligible to receive, rather than only the list of options the client has requested.",
    )  # --- IPAM alerting ---
    ipam_email_addresses: list[str] | None = Field(
        default=None,
        description="The e-mail lists to which the appliance sends IPAM threshold alarm e-mail messages.",
    )
    ipam_threshold_settings: dict[str, Any] | None = Field(
        default=None, description="IPAM utilization-threshold trigger settings."
    )
    ipam_trap_settings: dict[str, Any] | None = Field(
        default=None, description="IPAM utilization SNMP-trap settings."
    )  # --- lease ---
    lease_scavenge_time: int | None = Field(
        default=None,
        description="An integer that specifies the period of time (in seconds) that frees and backs up leases remained in the database before they are automatically deleted. To disable lease scavenging, set the parameter to -1. The minimum positive value must be greater than 86400 seconds (1 day).",
    )  # --- logic filters ---
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on the this network template. This list corresponds to the match rules that are written to the dhcpd configuration file.",
    )  # --- thresholds ---
    low_water_mark: int | None = Field(
        default=None,
        description="The percentage of DHCP network usage below which the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100.",
    )
    low_water_mark_reset: int | None = Field(
        default=None,
        description="The percentage of DHCP network usage threshold below which network usage is not expected and may warrant your attention. When the low watermark is crossed, the Infoblox appliance generates a syslog message and sends a warning (if enabled). A number that specifies the percentage of allocated addresses. The range is from 1 to 100. The low watermark reset value must be higher than the low watermark value.",
    )  # --- members (complex nested - list of dicts) ---
    members: list[dict[str, Any]] | None = Field(
        default=None,
        description='A list of members or Microsoft (r) servers that serve DHCP for this network. All members in the array must be of the same type. The struct type must be indicated in each element, by setting the "_struct" member to the struct type.',
    )  # --- core identity ---
    name: str | None = Field(default=None, description="The name of this network template.")
    netmask: int | None = Field(
        default=None, description="The netmask of the network in CIDR format."
    )  # --- nextserver ---
    nextserver: str | None = Field(
        default=None,
        description="The name in FQDN and/or IPv4 Address of the next server that the host needs to boot.",
    )  # --- DHCP options (complex nested - list of dicts) ---
    options: list[DhcpOption] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )  # --- PXE ---
    pxe_lease_time: int | None = Field(
        default=None,
        description="The PXE lease time value of a DHCP Network object. Some hosts use PXE (Preboot Execution Environment) to boot remotely from a server. To better manage your IP resources, set a different lease time for PXE boot requests. You can configure the DHCP server to allocate an IP address with a shorter lease time to hosts that send PXE boot requests, so IP addresses are not leased longer than necessary. A 32-bit unsigned integer that represents the duration, in seconds, for which the update is cached. Zero indicates that the update is not cached.",
    )  # --- range templates ---
    range_templates: list[str] | None = Field(
        default=None,
        description="The list of IP address range templates assigned to this network template object. When you create a network based on a network template object that contains range templates, the IP address ranges are created based on the associated IP address range templates.",
    )  # --- lease recycling ---
    recycle_leases: bool | None = Field(
        default=None,
        description="If the field is set to True, the leases are kept in the Recycle Bin until one week after expiration. Otherwise, the leases are permanently deleted.",
    )  # --- read-only ---
    rir: Literal["RIPE", "NONE"] | str | None = Field(
        default=None, description="The registry (RIR) that allocated the network address space."
    )  # --- RIR ---
    rir_organization: str | None = Field(
        default=None, description="The RIR organization associated with the network."
    )
    rir_registration_action: Literal["NONE", "CREATE"] | str | None = Field(
        default=None, description="The RIR registration action."
    )
    rir_registration_status: Literal["REGISTERED", "NOT_REGISTERED"] | str | None = Field(
        default=None, description="The registration status of the network in RIR."
    )
    send_rir_request: bool | None = Field(
        default=None, description="Determines whether to send the RIR registration request."
    )  # --- DNS on renewal ---
    update_dns_on_lease_renewal: bool | None = Field(
        default=None,
        description="This field controls whether the DHCP server updates DNS when a DHCP lease is renewed.",
    )  # --- use flags ---
    use_authority: bool | None = Field(default=None, description="Use flag for: authority")
    use_bootfile: bool | None = Field(default=None, description="Use flag for: bootfile")
    use_bootserver: bool | None = Field(default=None, description="Use flag for: bootserver")
    use_ddns_domainname: bool | None = Field(
        default=None, description="Use flag for: ddns_domainname"
    )
    use_ddns_generate_hostname: bool | None = Field(
        default=None, description="Use flag for: ddns_generate_hostname"
    )
    use_ddns_ttl: bool | None = Field(default=None, description="Use flag for: ddns_ttl")
    use_ddns_update_fixed_addresses: bool | None = Field(
        default=None, description="Use flag for: ddns_update_fixed_addresses"
    )
    use_ddns_use_option81: bool | None = Field(
        default=None, description="Use flag for: ddns_use_option81"
    )
    use_deny_bootp: bool | None = Field(default=None, description="Use flag for: deny_bootp")
    use_email_list: bool | None = Field(default=None, description="Use flag for: email_list")
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_enable_dhcp_thresholds: bool | None = Field(
        default=None, description="Use flag for: enable_dhcp_thresholds"
    )
    use_ignore_dhcp_option_list_request: bool | None = Field(
        default=None, description="Use flag for: ignore_dhcp_option_list_request"
    )
    use_ipam_email_addresses: bool | None = Field(
        default=None, description="Use flag for: ipam_email_addresses"
    )
    use_ipam_threshold_settings: bool | None = Field(
        default=None, description="Use flag for: ipam_threshold_settings"
    )
    use_ipam_trap_settings: bool | None = Field(
        default=None, description="Use flag for: ipam_trap_settings"
    )
    use_lease_scavenge_time: bool | None = Field(
        default=None, description="Use flag for: lease_scavenge_time"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_nextserver: bool | None = Field(default=None, description="Use flag for: nextserver")
    use_options: bool | None = Field(default=None, description="Use flag for: options")
    use_pxe_lease_time: bool | None = Field(
        default=None, description="Use flag for: pxe_lease_time"
    )
    use_recycle_leases: bool | None = Field(
        default=None, description="Use flag for: recycle_leases"
    )
    use_update_dns_on_lease_renewal: bool | None = Field(
        default=None, description="Use flag for: update_dns_on_lease_renewal"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
