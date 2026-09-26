# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Lease - NIOS DHCP lease (read-only aggregate).

All 37 properties from ``components.schemas.Lease`` in the v2.14 DHCP
swagger are represented here. All substantive fields are read-only.

NOTE: This is a read-only object in practice; WAPI will reject write attempts.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "billing_class",
        "binding_state",
        "client_hostname",
        "cltt",
        "discovered_data",
        "ends",
        "fingerprint",
        "hardware",
        "ipv6_duid",
        "ipv6_iaid",
        "ipv6_preferred_lifetime",
        "ipv6_prefix_bits",
        "is_invalid_mac",
        "ms_ad_user_data",
        "network",
        "network_view",
        "never_ends",
        "never_starts",
        "next_binding_state",
        "on_commit",
        "on_expiry",
        "on_release",
        "option",
        "protocol",
        "remote_id",
        "requested_options",
        "served_by",
        "server_host_name",
        "starts",
        "tsfp",
        "tstp",
        "uid",
        "username",
        "uuid",
        "variable",
    }
)


class Lease(BaseModel):
    """NIOS DHCP lease (read-only aggregate)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # all fields are read-only
    address: str | None = Field(
        default=None, description="The IPv4 Address or IPv6 Address of the lease."
    )
    billing_class: str | None = Field(
        default=None,
        description="The billing_class value of a DHCP Lease object. This field specifies the class to which this lease is currently billed. This field is for IPv4 leases only.",
    )
    binding_state: (
        Literal[
            "ABANDONED",
            "ACTIVE",
            "BACKUP",
            "DECLINED",
            "EXPIRED",
            "FREE",
            "OFFERED",
            "RELEASED",
            "RESET",
            "STATIC",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The binding state for the current lease. Following are some of the values this field can be set to: * ABANDONED: The Infoblox appliance cannot lease this IP address because the appliance received a response when it pinged the address. * ACTIVE: The lease is currently in use by a DHCP client. * EXPIRED: The lease was in use, but the DHCP client never renewed it, so it is no longer valid. * FREE: The lease is available for clients to use. * RELEASED: The DHCP client returned the lease to the appliance.",
    )
    client_hostname: str | None = Field(
        default=None,
        description="The client_hostname of a DHCP Lease object. This field specifies the host name that the DHCP client sends to the Infoblox appliance using DHCP option 12.",
    )
    cltt: int | None = Field(
        default=None,
        description="The CLTT (Client Last Transaction Time) value of a DHCP Lease object. This field specifies the time of the last transaction with the DHCP client for this lease.",
    )
    discovered_data: dict[str, Any] | None = Field(
        default=None, description="Discovered data populated by network discovery."
    )
    ends: int | None = Field(
        default=None,
        description="The end time value of a DHCP Lease object. This field specifies the time when a lease ended.",
    )
    fingerprint: str | None = Field(default=None, description="DHCP fingerprint for the lease.")
    hardware: str | None = Field(
        default=None,
        description="The hardware type of a DHCP Lease object. This field specifies the MAC address of the network interface on which the lease will be used. This field is supported for IPv4 leases, and from NIOS-9.0.6 onwards, also supported for IPv6 leases.",
    )
    ipv6_duid: str | None = Field(
        default=None,
        description="The DUID value for this lease. This field is only applicable for IPv6 leases.",
    )
    ipv6_iaid: str | None = Field(
        default=None,
        description="The interface ID of an IPv6 address that the Infoblox appliance leased to the DHCP client. This field is for IPv6 leases only.",
    )
    ipv6_preferred_lifetime: int | None = Field(
        default=None,
        description="The preferred lifetime value of an IPv6 address that the Infoblox appliance leased to the DHCP client. This field is for IPv6 leases only.",
    )
    ipv6_prefix_bits: int | None = Field(
        default=None, description="Prefix bits for this lease. This field is for IPv6 leases only."
    )
    is_invalid_mac: bool | None = Field(
        default=None,
        description="This flag reflects whether the MAC address for this lease is invalid.",
    )
    ms_ad_user_data: dict[str, Any] | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )
    network: str | None = Field(
        default=None,
        description='The network, in "network/netmask" format, with which this lease is associated.',
    )
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this lease resides."
    )
    never_ends: bool | None = Field(
        default=None,
        description="If this field is set to True, the lease does not have an end time.",
    )
    never_starts: bool | None = Field(
        default=None,
        description="If this field is set to True, the lease does not have a start time.",
    )
    next_binding_state: (
        Literal[
            "ABANDONED",
            "ACTIVE",
            "BACKUP",
            "DECLINED",
            "EXPIRED",
            "FREE",
            "OFFERED",
            "RELEASED",
            "RESET",
            "STATIC",
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The subsequent binding state when the current lease expires. This field is for IPv4 leases only. Following are some of the values this field can be set to: * ABANDONED: The Infoblox appliance cannot lease this IP address because the appliance received a response when it pinged the address. * ACTIVE: The lease is currently in use by a DHCP client. * EXPIRED: The lease was in use, but the DHCP client never renewed it, so it is no longer valid. * FREE: The lease is available for clients to use. * RELEASED: The DHCP client returned the lease to the appliance.",
    )
    on_commit: str | None = Field(
        default=None, description="The list of commands to be executed when the lease is granted."
    )
    on_expiry: str | None = Field(
        default=None, description="The list of commands to be executed when the lease expires."
    )
    on_release: str | None = Field(
        default=None, description="The list of commands to be executed when the lease is released."
    )
    option: str | None = Field(
        default=None,
        description="The option value of a DHCP Lease object. This field specifies the agent circuit ID and remote ID sent by a DHCP relay agent in DHCP option 82. This field is for IPv4 leases only.",
    )
    protocol: Literal["BOTH", "IPV4", "IPV6"] | str | None = Field(
        default=None,
        description="This field determines whether the lease is an IPv4 or IPv6 address.",
    )
    remote_id: str | None = Field(
        default=None,
        description='This field represents the "Remote ID" sub-option of DHCP option 82. Remote ID can be in ASCII form (e.g. ``"abcd"``) or in colon-separated HEX form (e.g. ``1:2:ab:cd``). HEX representation is used only when the sub-option value contains unprintable characters. If a remote ID sub-option value is in ASCII form, it is always enclosed in quotes to prevent ambiguous values (e.g. ``"10:20"`` - ASCII 5-byte string; ``10:20`` - HEX 2-byte value). * ASCII representation is used if the remote ID sub-option contains only printable ASCII characters (ASCII characters in range ``x20-0x7E``). * The backslash symbol (``\\``) is used as an escape symbol to escape the quote symbol (``"``) in an ASCII string. * Double backslashes (``\\\\``) are used to represent the backslash symbol (``\\``) in an ASCII string. * HEX representation is used only when the remote ID sub-option value contains unprintable characters and is normalized as follows: * starting zero is removed from digits: ``1``, ``a`` - Valid; ``01``, ``0a`` - Invalid; * lowercase characters are used for symbols: ``fa`` - Valid; ``FA`` - Invalid. NIOS does not support the convertion between HEX and ASCII formats. Searches are performed using the exact same format and value as the sub-option is represented. Query examples assume the following leases are stored in the database: .. tabularcolumns:: |p{1in}|p{3in}|p{2in}| ========= ========================== ============================ Number Option field Extracted remote ID field ========= ========================== ============================ Lease01 agent.remote-id= "00152654358700" "00152654358700" agent.circuit-id= "BX1-PORT-003" Lease02 agent.remote-id="Dhcp "Dhcp Relay 10" Relay 10" agent.circuit-id="Port008" Lease03 agent.remote-id="00:01:02" "00:01:02" Lease04 agent.remote-id=0:1:2 0:1:2 Lease05 agent.remote-id=02:03 2:3 Lease06 agent.remote-id=10:20 10:20 Lease07 agent.circuit-id= "no-remote-id" ========= ========================== ============================ Expected results: .. tabularcolumns:: |p{1.5in}|p{1.5in}|p{3in}| ========================= ==================== ============================= Query Returned leases Comments ========================= ==================== ============================= remote_id=01:02 None EXACT query. No results are expected. remote_id="Dhcp Relay 10" Lease02 EXACT query for an ASCII value. remote_id=0:1:2 Lease04 EXACT query for a HEX value. remote_id=00:01:02 None EXACT query for a HEX value. No results are expected as the search value is not normalized to the same format used in the database. remote_id~=10 Lease02, Lease06 REGEX query. remote_id~=^".*1 Lease01, Lease02, REGEX query. Only ASCII Lease03 values are expected due to the starting quote (``"``) in the search value. remote_id~=^[^"]*2 Lease04, Lease05, REGEX query. Only HEX values Lease06 are expected as the starting quote (``"``) is excluded from the search value. remote_id="" None EXACT query. No results are expected as no leases that contain an empty remote ID value exist in the database. ID value in the database. remote_id~="" Lease01, Lease02, REGEX query. This query is Lease03, Lease04, expected to match any Lease05, Lease06 lease that contain remote ID set to any value. ========================= ==================== ============================= **NOTE:** Lease07 is not expected to be returned when searching for the remote ID sub-option.',
    )
    requested_options: list[str] | str | None = Field(
        default=None,
        description='This field contains the option request list received from the client. For DHCPv4, it includes "Parameter Request List" data and for DHCPv6, it includes "Option Request Option" data.',
    )
    served_by: str | None = Field(
        default=None,
        description="The IP address of the server that sends an active lease to a client.",
    )
    server_host_name: str | None = Field(
        default=None,
        description="The host name of the Grid member or Microsoft DHCP server that issues the lease.",
    )
    starts: int | None = Field(
        default=None,
        description="The start time of a DHCP Lease object. This field specifies the time when the lease starts.",
    )
    tsfp: int | None = Field(
        default=None,
        description="The TSFP (Time Sent From Partner) value of a DHCP Lease object. This field specifies the time that the current lease state ends, from the point of view of a remote DHCP failover peer. This field is for IPv4 leases only.",
    )
    tstp: int | None = Field(
        default=None,
        description="The TSTP (Time Sent To Partner) value of a DHCP Lease object. This field specifies the time that the current lease state ends, from the point of view of a local DHCP failover peer. This field is for IPv4 leases only.",
    )
    uid: str | None = Field(
        default=None,
        description="The UID (User ID) value of a DHCP Lease object. This field specifies the client identifier that the DHCP client sends the Infoblox appliance (in DHCP option 61) when it acquires the lease. Not all DHCP clients send a UID. This field is for IPv4 leases only.",
    )
    username: str | None = Field(
        default=None,
        description="The user name that the server has associated with a DHCP Lease object.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    variable: str | None = Field(
        default=None,
        description="The variable value of a DHCP Lease object. This field keeps all variables related to the DDNS update of the DHCP lease. The variables related to the DDNS updates of the DHCP lease. The variables can be one of the following: ddns-text: The ddns-text variable is used to record the value of the client's TXT identification record when the interim DDNS update style has been used to update the DNS service for a particular lease. ddns-fwd-name: When a DDNS update was successfully completed, the ddns-fwd-name variable records the value of the name used when the client's A record was updated. The server may have used this name when it updated the client's PTR record. ddns-client-fqdn: If the server is configured to use the interim DDNS update style and is also configured to allow clients to update their own FQDNs, the ddns-client-fqdn variable records the name that the client used when it updated its own FQDN. This is also the name that the server used to update the client's PTR record. ddns-rev-name: If the server successfully updates the client's PTR record, this variable will record the name that the DHCP server used for the PTR record. The name to which the PTR record points will be either the ddns-fwd-name or the ddns-client-fqdn.",
    )
