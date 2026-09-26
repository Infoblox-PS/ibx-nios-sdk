# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DHCP domain - NIOS DHCP objects (ranges, fixed addresses, leases, etc.)."""

from __future__ import annotations

from ibx_nios_sdk.dhcp._dhcp_statistics import DhcpStatisticsResource
from ibx_nios_sdk.dhcp._dhcpfailover import DhcpfailoverResource
from ibx_nios_sdk.dhcp._dhcpoptiondefinition import DhcpoptiondefinitionResource
from ibx_nios_sdk.dhcp._dhcpoptionspace import DhcpoptionspaceResource
from ibx_nios_sdk.dhcp._filterfingerprint import FilterfingerprintResource
from ibx_nios_sdk.dhcp._filtermac import FiltermacResource
from ibx_nios_sdk.dhcp._filternac import FilternacResource
from ibx_nios_sdk.dhcp._filteroption import FilteroptionResource
from ibx_nios_sdk.dhcp._filterrelayagent import FilterrelayagentResource
from ibx_nios_sdk.dhcp._fingerprint import FingerprintResource
from ibx_nios_sdk.dhcp._fixedaddress import FixedaddressResource
from ibx_nios_sdk.dhcp._fixedaddresstemplate import FixedaddresstemplateResource
from ibx_nios_sdk.dhcp._ipv6dhcpoptiondefinition import Ipv6dhcpoptiondefinitionResource
from ibx_nios_sdk.dhcp._ipv6dhcpoptionspace import Ipv6dhcpoptionspaceResource
from ibx_nios_sdk.dhcp._ipv6filteroption import Ipv6filteroptionResource
from ibx_nios_sdk.dhcp._ipv6fixedaddress import Ipv6fixedaddressResource
from ibx_nios_sdk.dhcp._ipv6fixedaddresstemplate import Ipv6fixedaddresstemplateResource
from ibx_nios_sdk.dhcp._ipv6range import Ipv6rangeResource
from ibx_nios_sdk.dhcp._ipv6rangetemplate import Ipv6rangetemplateResource
from ibx_nios_sdk.dhcp._ipv6sharednetwork import Ipv6sharednetworkResource
from ibx_nios_sdk.dhcp._lease import LeaseResource
from ibx_nios_sdk.dhcp._macfilteraddress import MacfilteraddressResource
from ibx_nios_sdk.dhcp._orderedranges import OrderedrangesResource
from ibx_nios_sdk.dhcp._range import RangeResource
from ibx_nios_sdk.dhcp._rangetemplate import RangetemplateResource
from ibx_nios_sdk.dhcp._roaminghost import RoaminghostResource
from ibx_nios_sdk.dhcp._service import DhcpService
from ibx_nios_sdk.dhcp._sharednetwork import SharednetworkResource

__all__ = [
    "DhcpService",
    "DhcpStatisticsResource",
    "DhcpfailoverResource",
    "DhcpoptiondefinitionResource",
    "FingerprintResource",
    "LeaseResource",
    "MacfilteraddressResource",
    "RoaminghostResource",
    "DhcpoptionspaceResource",
    "FilterfingerprintResource",
    "Ipv6dhcpoptiondefinitionResource",
    "Ipv6dhcpoptionspaceResource",
    "FiltermacResource",
    "FilternacResource",
    "FilteroptionResource",
    "FilterrelayagentResource",
    "FixedaddressResource",
    "Ipv6filteroptionResource",
    "Ipv6sharednetworkResource",
    "SharednetworkResource",
    "FixedaddresstemplateResource",
    "Ipv6fixedaddressResource",
    "Ipv6fixedaddresstemplateResource",
    "Ipv6rangeResource",
    "Ipv6rangetemplateResource",
    "OrderedrangesResource",
    "RangeResource",
    "RangetemplateResource",
]
