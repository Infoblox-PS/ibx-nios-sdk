# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MicrosoftserverService - entry point for Microsoft server resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.microsoftserver._msserver import MsserverResource
    from ibx_nios_sdk.microsoftserver._msserver_adsites_domain import MsserverAdsitesDomainResource
    from ibx_nios_sdk.microsoftserver._msserver_adsites_site import MsserverAdsitesSiteResource
    from ibx_nios_sdk.microsoftserver._msserver_dhcp import MsserverDhcpResource
    from ibx_nios_sdk.microsoftserver._msserver_dns import MsserverDnsResource
    from ibx_nios_sdk.microsoftserver._mssuperscope import MssuperscopeResource


class MicrosoftserverService:
    """Entry point for NIOS Microsoft server resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise MicrosoftserverService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def msserver(self) -> MsserverResource:
        """Entry point for NIOS Microsoft server resources."""
        from ibx_nios_sdk.microsoftserver._msserver import MsserverResource

        return MsserverResource(self._client)

    @cached_property
    def adsites_domain(self) -> MsserverAdsitesDomainResource:
        """Entry point for NIOS Microsoft server AD sites domain resources."""
        from ibx_nios_sdk.microsoftserver._msserver_adsites_domain import (
            MsserverAdsitesDomainResource,
        )

        return MsserverAdsitesDomainResource(self._client)

    @cached_property
    def adsites_site(self) -> MsserverAdsitesSiteResource:
        """Entry point for NIOS Microsoft server AD sites site resources."""
        from ibx_nios_sdk.microsoftserver._msserver_adsites_site import MsserverAdsitesSiteResource

        return MsserverAdsitesSiteResource(self._client)

    @cached_property
    def dhcp(self) -> MsserverDhcpResource:
        """Entry point for NIOS Microsoft server DHCP configuration resources."""
        from ibx_nios_sdk.microsoftserver._msserver_dhcp import MsserverDhcpResource

        return MsserverDhcpResource(self._client)

    @cached_property
    def dns(self) -> MsserverDnsResource:
        """Entry point for NIOS Microsoft server DNS configuration resources."""
        from ibx_nios_sdk.microsoftserver._msserver_dns import MsserverDnsResource

        return MsserverDnsResource(self._client)

    @cached_property
    def mssuperscope(self) -> MssuperscopeResource:
        """Entry point for NIOS Microsoft server superscope resources."""
        from ibx_nios_sdk.microsoftserver._mssuperscope import MssuperscopeResource

        return MssuperscopeResource(self._client)
