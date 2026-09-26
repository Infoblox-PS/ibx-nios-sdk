# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""IpamService - entry point for IPAM resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.ipam._bulkhost import BulkhostResource
    from ibx_nios_sdk.ipam._bulkhostnametemplate import BulkhostnametemplateResource
    from ibx_nios_sdk.ipam._discoverytask import DiscoverytaskResource
    from ibx_nios_sdk.ipam._hostnamerewritepolicy import HostnamerewritepolicyResource
    from ibx_nios_sdk.ipam._ipam_statistics import IpamStatisticsResource
    from ibx_nios_sdk.ipam._ipv4address import Ipv4addressResource
    from ibx_nios_sdk.ipam._ipv6address import Ipv6addressResource
    from ibx_nios_sdk.ipam._ipv6network import Ipv6networkResource
    from ibx_nios_sdk.ipam._ipv6networkcontainer import Ipv6networkcontainerResource
    from ibx_nios_sdk.ipam._ipv6networktemplate import Ipv6networktemplateResource
    from ibx_nios_sdk.ipam._network import NetworkResource
    from ibx_nios_sdk.ipam._network_discovery import NetworkDiscoveryResource
    from ibx_nios_sdk.ipam._networkcontainer import NetworkcontainerResource
    from ibx_nios_sdk.ipam._networktemplate import NetworktemplateResource
    from ibx_nios_sdk.ipam._networkview import NetworkviewResource
    from ibx_nios_sdk.ipam._rir import RirResource
    from ibx_nios_sdk.ipam._rir_organization import RirOrganizationResource
    from ibx_nios_sdk.ipam._superhost import SuperhostResource
    from ibx_nios_sdk.ipam._superhostchild import SuperhostchildResource
    from ibx_nios_sdk.ipam._vlan import VlanResource
    from ibx_nios_sdk.ipam._vlanrange import VlanrangeResource
    from ibx_nios_sdk.ipam._vlanview import VlanviewResource


class IpamService:
    """Entry point for NIOS IPAM resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise IpamService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def networkview(self) -> NetworkviewResource:
        """Entry point for NIOS IPAM network view resources."""
        from ibx_nios_sdk.ipam._networkview import NetworkviewResource

        return NetworkviewResource(self._client)

    @cached_property
    def network(self) -> NetworkResource:
        """Entry point for NIOS IPAM IPv4 network resources."""
        from ibx_nios_sdk.ipam._network import NetworkResource

        return NetworkResource(self._client)

    @cached_property
    def networkcontainer(self) -> NetworkcontainerResource:
        """Entry point for NIOS IPAM IPv4 network container resources."""
        from ibx_nios_sdk.ipam._networkcontainer import NetworkcontainerResource

        return NetworkcontainerResource(self._client)

    @cached_property
    def networktemplate(self) -> NetworktemplateResource:
        """Entry point for NIOS IPAM IPv4 network template resources."""
        from ibx_nios_sdk.ipam._networktemplate import NetworktemplateResource

        return NetworktemplateResource(self._client)

    @cached_property
    def ipv4address(self) -> Ipv4addressResource:
        """Entry point for NIOS IPAM IPv4 address resources."""
        from ibx_nios_sdk.ipam._ipv4address import Ipv4addressResource

        return Ipv4addressResource(self._client)

    @cached_property
    def ipv6network(self) -> Ipv6networkResource:
        """Entry point for NIOS IPAM IPv6 network resources."""
        from ibx_nios_sdk.ipam._ipv6network import Ipv6networkResource

        return Ipv6networkResource(self._client)

    @cached_property
    def ipv6networkcontainer(self) -> Ipv6networkcontainerResource:
        """Entry point for NIOS IPAM IPv6 network container resources."""
        from ibx_nios_sdk.ipam._ipv6networkcontainer import Ipv6networkcontainerResource

        return Ipv6networkcontainerResource(self._client)

    @cached_property
    def ipv6networktemplate(self) -> Ipv6networktemplateResource:
        """Entry point for NIOS IPAM IPv6 network template resources."""
        from ibx_nios_sdk.ipam._ipv6networktemplate import Ipv6networktemplateResource

        return Ipv6networktemplateResource(self._client)

    @cached_property
    def ipv6address(self) -> Ipv6addressResource:
        """Entry point for NIOS IPAM IPv6 address resources."""
        from ibx_nios_sdk.ipam._ipv6address import Ipv6addressResource

        return Ipv6addressResource(self._client)

    @cached_property
    def vlan(self) -> VlanResource:
        """Entry point for NIOS VLAN resources."""
        from ibx_nios_sdk.ipam._vlan import VlanResource

        return VlanResource(self._client)

    @cached_property
    def vlanview(self) -> VlanviewResource:
        """Entry point for NIOS VLAN view resources."""
        from ibx_nios_sdk.ipam._vlanview import VlanviewResource

        return VlanviewResource(self._client)

    @cached_property
    def vlanrange(self) -> VlanrangeResource:
        """Entry point for NIOS VLAN range resources."""
        from ibx_nios_sdk.ipam._vlanrange import VlanrangeResource

        return VlanrangeResource(self._client)

    @cached_property
    def bulkhost(self) -> BulkhostResource:
        """Entry point for NIOS IPAM bulk host resources."""
        from ibx_nios_sdk.ipam._bulkhost import BulkhostResource

        return BulkhostResource(self._client)

    @cached_property
    def bulkhostnametemplate(self) -> BulkhostnametemplateResource:
        """Entry point for NIOS IPAM bulk host name template resources."""
        from ibx_nios_sdk.ipam._bulkhostnametemplate import BulkhostnametemplateResource

        return BulkhostnametemplateResource(self._client)

    @cached_property
    def discovery_discoverytask(self) -> DiscoverytaskResource:
        """Entry point for NIOS network discovery task resources."""
        from ibx_nios_sdk.ipam._discoverytask import DiscoverytaskResource

        return DiscoverytaskResource(self._client)

    @cached_property
    def network_discovery(self) -> NetworkDiscoveryResource:
        """Entry point for NIOS network discovery result resources."""
        from ibx_nios_sdk.ipam._network_discovery import NetworkDiscoveryResource

        return NetworkDiscoveryResource(self._client)

    @cached_property
    def superhost(self) -> SuperhostResource:
        """Entry point for NIOS IPAM superhost resources."""
        from ibx_nios_sdk.ipam._superhost import SuperhostResource

        return SuperhostResource(self._client)

    @cached_property
    def superhostchild(self) -> SuperhostchildResource:
        """Entry point for NIOS IPAM superhost child resources."""
        from ibx_nios_sdk.ipam._superhostchild import SuperhostchildResource

        return SuperhostchildResource(self._client)

    @cached_property
    def hostnamerewritepolicy(self) -> HostnamerewritepolicyResource:
        """Entry point for NIOS IPAM hostname rewrite policy resources."""
        from ibx_nios_sdk.ipam._hostnamerewritepolicy import HostnamerewritepolicyResource

        return HostnamerewritepolicyResource(self._client)

    @cached_property
    def rir(self) -> RirResource:
        """Entry point for NIOS Regional Internet Registry (RIR) resources."""
        from ibx_nios_sdk.ipam._rir import RirResource

        return RirResource(self._client)

    @cached_property
    def rir_organization(self) -> RirOrganizationResource:
        """Entry point for NIOS RIR organization resources."""
        from ibx_nios_sdk.ipam._rir_organization import RirOrganizationResource

        return RirOrganizationResource(self._client)

    @cached_property
    def ipam_statistics(self) -> IpamStatisticsResource:
        """Entry point for NIOS IPAM statistics resources."""
        from ibx_nios_sdk.ipam._ipam_statistics import IpamStatisticsResource

        return IpamStatisticsResource(self._client)
