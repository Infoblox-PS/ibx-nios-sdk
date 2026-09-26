# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryService - entry point for discovery resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.discovery._discovery import DiscoveryResource
    from ibx_nios_sdk.discovery._discovery_credentialgroup import DiscoveryCredentialgroupResource
    from ibx_nios_sdk.discovery._discovery_device import DiscoveryDeviceResource
    from ibx_nios_sdk.discovery._discovery_devicecomponent import DiscoveryDevicecomponentResource
    from ibx_nios_sdk.discovery._discovery_deviceinterface import DiscoveryDeviceinterfaceResource
    from ibx_nios_sdk.discovery._discovery_deviceneighbor import DiscoveryDeviceneighborResource
    from ibx_nios_sdk.discovery._discovery_devicesupportbundle import (
        DiscoveryDevicesupportbundleResource,
    )
    from ibx_nios_sdk.discovery._discovery_diagnostictask import DiscoveryDiagnostictaskResource
    from ibx_nios_sdk.discovery._discovery_gridproperties import DiscoveryGridpropertiesResource
    from ibx_nios_sdk.discovery._discovery_memberproperties import (
        DiscoveryMemberpropertiesResource,
    )
    from ibx_nios_sdk.discovery._discovery_sdnnetwork import DiscoverySdnnetworkResource
    from ibx_nios_sdk.discovery._discovery_status import DiscoveryStatusResource
    from ibx_nios_sdk.discovery._discovery_vrf import DiscoveryVrfResource
    from ibx_nios_sdk.discovery._vdiscoverytask import VdiscoverytaskResource


class DiscoveryService:
    """Entry point for NIOS discovery resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise DiscoveryService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def discovery(self) -> DiscoveryResource:
        """Entry point for NIOS network discovery global configuration resources."""
        from ibx_nios_sdk.discovery._discovery import DiscoveryResource

        return DiscoveryResource(self._client)

    @cached_property
    def credentialgroup(self) -> DiscoveryCredentialgroupResource:
        """Entry point for NIOS network discovery credential group resources."""
        from ibx_nios_sdk.discovery._discovery_credentialgroup import (
            DiscoveryCredentialgroupResource,
        )

        return DiscoveryCredentialgroupResource(self._client)

    @cached_property
    def device(self) -> DiscoveryDeviceResource:
        """Entry point for NIOS network discovery device resources."""
        from ibx_nios_sdk.discovery._discovery_device import DiscoveryDeviceResource

        return DiscoveryDeviceResource(self._client)

    @cached_property
    def devicecomponent(self) -> DiscoveryDevicecomponentResource:
        """Entry point for NIOS network discovery device component resources."""
        from ibx_nios_sdk.discovery._discovery_devicecomponent import (
            DiscoveryDevicecomponentResource,
        )

        return DiscoveryDevicecomponentResource(self._client)

    @cached_property
    def deviceinterface(self) -> DiscoveryDeviceinterfaceResource:
        """Entry point for NIOS network discovery device interface resources."""
        from ibx_nios_sdk.discovery._discovery_deviceinterface import (
            DiscoveryDeviceinterfaceResource,
        )

        return DiscoveryDeviceinterfaceResource(self._client)

    @cached_property
    def deviceneighbor(self) -> DiscoveryDeviceneighborResource:
        """Entry point for NIOS network discovery device neighbor resources."""
        from ibx_nios_sdk.discovery._discovery_deviceneighbor import (
            DiscoveryDeviceneighborResource,
        )

        return DiscoveryDeviceneighborResource(self._client)

    @cached_property
    def devicesupportbundle(self) -> DiscoveryDevicesupportbundleResource:
        """Entry point for NIOS network discovery device support bundle resources."""
        from ibx_nios_sdk.discovery._discovery_devicesupportbundle import (
            DiscoveryDevicesupportbundleResource,
        )

        return DiscoveryDevicesupportbundleResource(self._client)

    @cached_property
    def diagnostictask(self) -> DiscoveryDiagnostictaskResource:
        """Entry point for NIOS network discovery diagnostic task resources."""
        from ibx_nios_sdk.discovery._discovery_diagnostictask import (
            DiscoveryDiagnostictaskResource,
        )

        return DiscoveryDiagnostictaskResource(self._client)

    @cached_property
    def gridproperties(self) -> DiscoveryGridpropertiesResource:
        """Entry point for NIOS network discovery grid properties resources."""
        from ibx_nios_sdk.discovery._discovery_gridproperties import (
            DiscoveryGridpropertiesResource,
        )

        return DiscoveryGridpropertiesResource(self._client)

    @cached_property
    def memberproperties(self) -> DiscoveryMemberpropertiesResource:
        """Entry point for NIOS network discovery member properties resources."""
        from ibx_nios_sdk.discovery._discovery_memberproperties import (
            DiscoveryMemberpropertiesResource,
        )

        return DiscoveryMemberpropertiesResource(self._client)

    @cached_property
    def sdnnetwork(self) -> DiscoverySdnnetworkResource:
        """Entry point for NIOS network discovery SDN network resources."""
        from ibx_nios_sdk.discovery._discovery_sdnnetwork import DiscoverySdnnetworkResource

        return DiscoverySdnnetworkResource(self._client)

    @cached_property
    def status(self) -> DiscoveryStatusResource:
        """Entry point for NIOS network discovery status resources."""
        from ibx_nios_sdk.discovery._discovery_status import DiscoveryStatusResource

        return DiscoveryStatusResource(self._client)

    @cached_property
    def vrf(self) -> DiscoveryVrfResource:
        """Entry point for NIOS network discovery VRF resources."""
        from ibx_nios_sdk.discovery._discovery_vrf import DiscoveryVrfResource

        return DiscoveryVrfResource(self._client)

    @cached_property
    def vdiscoverytask(self) -> VdiscoverytaskResource:
        """Entry point for NIOS vDiscovery task resources."""
        from ibx_nios_sdk.discovery._vdiscoverytask import VdiscoverytaskResource

        return VdiscoverytaskResource(self._client)
