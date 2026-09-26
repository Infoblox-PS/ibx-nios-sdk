# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6range - NIOS DHCP IPv6 range.

All 51 properties from ``components.schemas.Ipv6range`` in the v2.14 DHCP
swagger are represented here. Deeply nested types are inlined as dicts.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue, LogicFilterRule, MsDhcpOption

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "discover_now_status",
        "endpoint_sources",
        "uuid",
    }
)


class Ipv6range(BaseModel):
    """NIOS DHCP IPv6 range."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    address_type: str | None = Field(
        default=None,
        description="Type of a DHCP IPv6 Range object. Valid values are \"ADDRESS\", \"PREFIX\", or \"BOTH\". When the address type is \"ADDRESS\", values for the 'start_addr' and 'end_addr' members are required. When the address type is \"PREFIX\", values for 'ipv6_start_prefix', 'ipv6_end_prefix', and 'ipv6_prefix_bits' are required. When the address type is \"BOTH\", values for 'start_addr', 'end_addr', 'ipv6_start_prefix', 'ipv6_end_prefix', and 'ipv6_prefix_bits' are all required.",
    )
    always_update_dns: bool | None = Field(
        default=None,
        description="This field controls whether only the DHCPv6 server is allowed to update DNS, regardless of the DHCPv6 client requests.",
    )
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )
    comment: str | None = Field(
        default=None, description="Comment for the range; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a range is disabled or not. When this is set to False, the range is enabled.",
    )  # read-only
    discover_now_status: (
        Literal["NONE", "PENDING", "RUNNING", "COMPLETE", "FAILED"] | str | None
    ) = Field(default=None, description="Discover now status for this range.")
    discovery_basic_poll_settings: dict[str, Any] | None = Field(
        default=None, description="Basic discovery polling settings."
    )
    discovery_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Discovery blackout schedule for this object."
    )
    discovery_member: str | None = Field(
        default=None, description="The member that will run discovery for this range."
    )
    enable_ddns: bool | None = Field(
        default=None,
        description="The dynamic DNS updates flag of a DHCP IPv6 range object. If set to True, the DHCPv6 server sends DDNS updates to DNS servers in the same Grid, and to external DNS servers.",
    )
    enable_discovery: bool | None = Field(
        default=None,
        description="Determines whether a discovery is enabled or not for this range. When this is set to False, the discovery for this range is disabled.",
    )
    enable_immediate_discovery: bool | None = Field(
        default=None,
        description="Determines if the discovery for the range should be immediately enabled.",
    )
    end_addr: str | None = Field(
        default=None, description="The IPv6 Address end address of the DHCP IPv6 range."
    )  # read-only
    endpoint_sources: list[dict[str, Any] | str] | None = Field(
        default=None,
        description="The endpoints that provides data for the DHCP IPv6 Range object.",
    )
    exclude: list[dict[str, Any]] | None = Field(
        default=None,
        description="These are ranges of IP addresses that the appliance does not use to assign to clients. You can use these exclusion addresses as static IP addresses. They contain the start and end addresses of the exclusion range, and optionally,information about this exclusion range.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    ipv6_end_prefix: str | None = Field(
        default=None, description="The IPv6 Address end prefix of the DHCP IPv6 range."
    )
    ipv6_prefix_bits: int | None = Field(
        default=None, description="Prefix bits of the DHCP IPv6 range."
    )
    ipv6_start_prefix: str | None = Field(
        default=None, description="The IPv6 Address starting prefix of the DHCP IPv6 range."
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied to this IPv6 range. This list corresponds to the match rules that are written to the DHCPv6 configuration file.",
    )
    member: dict[str, Any] | None = Field(
        default=None, description="Reference to the Grid member that hosts this object."
    )
    ms_options: list[MsDhcpOption] | None = Field(
        default=None,
        description="This field contains the Microsoft DHCP options for this IPv6 range.",
    )
    ms_preference: int | None = Field(
        default=None, description="This field contains the MS preference for this IPv6 Range."
    )
    ms_server: dict[str, Any] | None = Field(
        default=None, description="The primary Microsoft Server."
    )
    name: str | None = Field(
        default=None, description="This field contains the name of the Microsoft scope."
    )
    network: str | None = Field(
        default=None, description="The network this range belongs to, in IPv6 Address/CIDR format."
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this range resides."
    )
    next_available_ip: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the next-available-IP operation."
    )
    option_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the Option filters to be applied to this IPv6 range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    port_control_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Port-control blackout schedule for this object."
    )
    preferred_lifetime: int | None = Field(
        default=None, description="This field contains the IPv6 preferred lifetime."
    )
    recycle_leases: bool | None = Field(
        default=None,
        description="If the field is set to True, the leases are kept in the Recycle Bin until one week after expiration. Otherwise, the leases are permanently deleted.",
    )
    restart_if_needed: bool | None = Field(
        default=None, description="Restarts the member service."
    )
    same_port_control_discovery_blackout: bool | None = Field(
        default=None,
        description="If the field is set to True, the discovery blackout setting will be used for port control blackout setting.",
    )
    server_association_type: Literal["NONE", "MEMBER", "MS_SERVER"] | str | None = Field(
        default=None, description="The type of server that is going to serve the range."
    )
    start_addr: str | None = Field(
        default=None, description="The IPv6 Address starting address of the DHCP IPv6 range."
    )
    subscribe_settings: dict[str, Any] | None = Field(
        default=None,
        description="Subscription settings for receiving updates from upstream sources.",
    )
    template: str | None = Field(
        default=None,
        description="If set on creation, the range will be created according to the values specified in the named template.",
    )
    use_blackout_setting: bool | None = Field(
        default=None,
        description="Use flag for: discovery_blackout_setting , port_control_blackout_setting, same_port_control_discovery_blackout",
    )
    use_discovery_basic_polling_settings: bool | None = Field(
        default=None, description="Use flag for: discovery_basic_poll_settings"
    )
    use_enable_ddns: bool | None = Field(default=None, description="Use flag for: enable_ddns")
    use_enable_discovery: bool | None = Field(
        default=None, description="Use flag for: discovery_member , enable_discovery"
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_ms_options: bool | None = Field(default=None, description="Use flag for: ms_options")
    use_preferred_lifetime: bool | None = Field(
        default=None, description="Use flag for: preferred_lifetime"
    )
    use_recycle_leases: bool | None = Field(
        default=None, description="Use flag for: recycle_leases"
    )
    use_subscribe_settings: bool | None = Field(
        default=None, description="Use flag for: subscribe_settings"
    )
    use_valid_lifetime: bool | None = Field(
        default=None, description="Use flag for: valid_lifetime"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    valid_lifetime: int | None = Field(
        default=None, description="This field contains the IPv6 valid lifetime."
    )
