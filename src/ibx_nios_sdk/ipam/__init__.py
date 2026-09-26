# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""IPAM domain - NIOS IPAM objects (networks, addresses, ranges, etc.)."""

from __future__ import annotations

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
from ibx_nios_sdk.ipam._service import IpamService
from ibx_nios_sdk.ipam._superhost import SuperhostResource
from ibx_nios_sdk.ipam._superhostchild import SuperhostchildResource
from ibx_nios_sdk.ipam._vlan import VlanResource
from ibx_nios_sdk.ipam._vlanrange import VlanrangeResource
from ibx_nios_sdk.ipam._vlanview import VlanviewResource

__all__ = [
    "BulkhostResource",
    "BulkhostnametemplateResource",
    "DiscoverytaskResource",
    "HostnamerewritepolicyResource",
    "IpamService",
    "IpamStatisticsResource",
    "Ipv4addressResource",
    "Ipv6addressResource",
    "Ipv6networkResource",
    "Ipv6networkcontainerResource",
    "Ipv6networktemplateResource",
    "NetworkDiscoveryResource",
    "NetworkResource",
    "NetworkcontainerResource",
    "NetworktemplateResource",
    "NetworkviewResource",
    "RirOrganizationResource",
    "RirResource",
    "SuperhostResource",
    "SuperhostchildResource",
    "VlanResource",
    "VlanrangeResource",
    "VlanviewResource",
]
