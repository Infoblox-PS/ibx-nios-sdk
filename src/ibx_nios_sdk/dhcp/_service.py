# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpService - entry point for DHCP resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
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
    from ibx_nios_sdk.dhcp._sharednetwork import SharednetworkResource


class DhcpService:
    """Entry point for NIOS DHCP resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise DhcpService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def range(self) -> RangeResource:
        """Entry point for NIOS DHCP IPv4 range resources."""
        from ibx_nios_sdk.dhcp._range import RangeResource

        return RangeResource(self._client)

    @cached_property
    def rangetemplate(self) -> RangetemplateResource:
        """Entry point for NIOS DHCP range template resources."""
        from ibx_nios_sdk.dhcp._rangetemplate import RangetemplateResource

        return RangetemplateResource(self._client)

    @cached_property
    def ipv6range(self) -> Ipv6rangeResource:
        """Entry point for NIOS DHCPv6 range resources."""
        from ibx_nios_sdk.dhcp._ipv6range import Ipv6rangeResource

        return Ipv6rangeResource(self._client)

    @cached_property
    def ipv6rangetemplate(self) -> Ipv6rangetemplateResource:
        """Entry point for NIOS DHCPv6 range template resources."""
        from ibx_nios_sdk.dhcp._ipv6rangetemplate import Ipv6rangetemplateResource

        return Ipv6rangetemplateResource(self._client)

    @cached_property
    def orderedranges(self) -> OrderedrangesResource:
        """Entry point for NIOS DHCP ordered ranges resources."""
        from ibx_nios_sdk.dhcp._orderedranges import OrderedrangesResource

        return OrderedrangesResource(self._client)

    @cached_property
    def fixedaddress(self) -> FixedaddressResource:
        """Entry point for NIOS DHCP fixed address resources."""
        from ibx_nios_sdk.dhcp._fixedaddress import FixedaddressResource

        return FixedaddressResource(self._client)

    @cached_property
    def fixedaddresstemplate(self) -> FixedaddresstemplateResource:
        """Entry point for NIOS DHCP fixed address template resources."""
        from ibx_nios_sdk.dhcp._fixedaddresstemplate import FixedaddresstemplateResource

        return FixedaddresstemplateResource(self._client)

    @cached_property
    def ipv6fixedaddress(self) -> Ipv6fixedaddressResource:
        """Entry point for NIOS DHCPv6 fixed address resources."""
        from ibx_nios_sdk.dhcp._ipv6fixedaddress import Ipv6fixedaddressResource

        return Ipv6fixedaddressResource(self._client)

    @cached_property
    def ipv6fixedaddresstemplate(self) -> Ipv6fixedaddresstemplateResource:
        """Entry point for NIOS DHCPv6 fixed address template resources."""
        from ibx_nios_sdk.dhcp._ipv6fixedaddresstemplate import Ipv6fixedaddresstemplateResource

        return Ipv6fixedaddresstemplateResource(self._client)

    @cached_property
    def sharednetwork(self) -> SharednetworkResource:
        """Entry point for NIOS DHCP shared network resources."""
        from ibx_nios_sdk.dhcp._sharednetwork import SharednetworkResource

        return SharednetworkResource(self._client)

    @cached_property
    def ipv6sharednetwork(self) -> Ipv6sharednetworkResource:
        """Entry point for NIOS DHCPv6 shared network resources."""
        from ibx_nios_sdk.dhcp._ipv6sharednetwork import Ipv6sharednetworkResource

        return Ipv6sharednetworkResource(self._client)

    @cached_property
    def filterfingerprint(self) -> FilterfingerprintResource:
        """Entry point for NIOS DHCP fingerprint filter resources."""
        from ibx_nios_sdk.dhcp._filterfingerprint import FilterfingerprintResource

        return FilterfingerprintResource(self._client)

    @cached_property
    def filtermac(self) -> FiltermacResource:
        """Entry point for NIOS DHCP MAC address filter resources."""
        from ibx_nios_sdk.dhcp._filtermac import FiltermacResource

        return FiltermacResource(self._client)

    @cached_property
    def filternac(self) -> FilternacResource:
        """Entry point for NIOS DHCP NAC filter resources."""
        from ibx_nios_sdk.dhcp._filternac import FilternacResource

        return FilternacResource(self._client)

    @cached_property
    def filteroption(self) -> FilteroptionResource:
        """Entry point for NIOS DHCP option filter resources."""
        from ibx_nios_sdk.dhcp._filteroption import FilteroptionResource

        return FilteroptionResource(self._client)

    @cached_property
    def filterrelayagent(self) -> FilterrelayagentResource:
        """Entry point for NIOS DHCP relay agent filter resources."""
        from ibx_nios_sdk.dhcp._filterrelayagent import FilterrelayagentResource

        return FilterrelayagentResource(self._client)

    @cached_property
    def ipv6filteroption(self) -> Ipv6filteroptionResource:
        """Entry point for NIOS DHCPv6 option filter resources."""
        from ibx_nios_sdk.dhcp._ipv6filteroption import Ipv6filteroptionResource

        return Ipv6filteroptionResource(self._client)

    @cached_property
    def dhcpoptiondefinition(self) -> DhcpoptiondefinitionResource:
        """Entry point for NIOS DHCP option definition resources."""
        from ibx_nios_sdk.dhcp._dhcpoptiondefinition import DhcpoptiondefinitionResource

        return DhcpoptiondefinitionResource(self._client)

    @cached_property
    def dhcpoptionspace(self) -> DhcpoptionspaceResource:
        """Entry point for NIOS DHCP option space resources."""
        from ibx_nios_sdk.dhcp._dhcpoptionspace import DhcpoptionspaceResource

        return DhcpoptionspaceResource(self._client)

    @cached_property
    def ipv6dhcpoptiondefinition(self) -> Ipv6dhcpoptiondefinitionResource:
        """Entry point for NIOS DHCPv6 option definition resources."""
        from ibx_nios_sdk.dhcp._ipv6dhcpoptiondefinition import Ipv6dhcpoptiondefinitionResource

        return Ipv6dhcpoptiondefinitionResource(self._client)

    @cached_property
    def ipv6dhcpoptionspace(self) -> Ipv6dhcpoptionspaceResource:
        """Entry point for NIOS DHCPv6 option space resources."""
        from ibx_nios_sdk.dhcp._ipv6dhcpoptionspace import Ipv6dhcpoptionspaceResource

        return Ipv6dhcpoptionspaceResource(self._client)

    @cached_property
    def dhcpfailover(self) -> DhcpfailoverResource:
        """Entry point for NIOS DHCP failover association resources."""
        from ibx_nios_sdk.dhcp._dhcpfailover import DhcpfailoverResource

        return DhcpfailoverResource(self._client)

    @cached_property
    def fingerprint(self) -> FingerprintResource:
        """Entry point for NIOS DHCP fingerprint resources."""
        from ibx_nios_sdk.dhcp._fingerprint import FingerprintResource

        return FingerprintResource(self._client)

    @cached_property
    def lease(self) -> LeaseResource:
        """Entry point for NIOS DHCP lease resources."""
        from ibx_nios_sdk.dhcp._lease import LeaseResource

        return LeaseResource(self._client)

    @cached_property
    def macfilteraddress(self) -> MacfilteraddressResource:
        """Entry point for NIOS DHCP MAC filter address resources."""
        from ibx_nios_sdk.dhcp._macfilteraddress import MacfilteraddressResource

        return MacfilteraddressResource(self._client)

    @cached_property
    def roaminghost(self) -> RoaminghostResource:
        """Entry point for NIOS DHCP roaming host resources."""
        from ibx_nios_sdk.dhcp._roaminghost import RoaminghostResource

        return RoaminghostResource(self._client)

    @cached_property
    def dhcp_statistics(self) -> DhcpStatisticsResource:
        """Entry point for NIOS DHCP statistics resources."""
        from ibx_nios_sdk.dhcp._dhcp_statistics import DhcpStatisticsResource

        return DhcpStatisticsResource(self._client)
