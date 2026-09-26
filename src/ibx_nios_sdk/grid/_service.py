# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridService - entry point for Grid resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.grid._captiveportal import CaptiveportalResource
    from ibx_nios_sdk.grid._distributionschedule import DistributionscheduleResource
    from ibx_nios_sdk.grid._extensibleattributedef import ExtensibleattributedefResource
    from ibx_nios_sdk.grid._gmcgroup import GmcgroupResource
    from ibx_nios_sdk.grid._gmcschedule import GmcscheduleResource
    from ibx_nios_sdk.grid._grid import GridResource
    from ibx_nios_sdk.grid._grid_cloudapi import GridCloudapiResource
    from ibx_nios_sdk.grid._grid_cloudapi_cloudstatistics import (
        GridCloudapiCloudstatisticsResource,
    )
    from ibx_nios_sdk.grid._grid_cloudapi_tenant import GridCloudapiTenantResource
    from ibx_nios_sdk.grid._grid_cloudapi_vm import GridCloudapiVmResource
    from ibx_nios_sdk.grid._grid_cloudapi_vmaddress import GridCloudapiVmaddressResource
    from ibx_nios_sdk.grid._grid_dashboard import GridDashboardResource
    from ibx_nios_sdk.grid._grid_dhcpproperties import GridDhcppropertiesResource
    from ibx_nios_sdk.grid._grid_dns import GridDnsResource
    from ibx_nios_sdk.grid._grid_filedistribution import GridFiledistributionResource
    from ibx_nios_sdk.grid._grid_license_pool import GridLicensePoolResource
    from ibx_nios_sdk.grid._grid_license_pool_container import GridLicensePoolContainerResource
    from ibx_nios_sdk.grid._grid_maxminddbinfo import GridMaxminddbinfoResource
    from ibx_nios_sdk.grid._grid_member_cloudapi import GridMemberCloudapiResource
    from ibx_nios_sdk.grid._grid_servicerestart_group import GridServicerestartGroupResource
    from ibx_nios_sdk.grid._grid_servicerestart_group_order import (
        GridServicerestartGroupOrderResource,
    )
    from ibx_nios_sdk.grid._grid_servicerestart_request import GridServicerestartRequestResource
    from ibx_nios_sdk.grid._grid_servicerestart_request_changedobject import (
        GridServicerestartRequestChangedobjectResource,
    )
    from ibx_nios_sdk.grid._grid_servicerestart_status import GridServicerestartStatusResource
    from ibx_nios_sdk.grid._grid_threatinsight import GridThreatinsightResource
    from ibx_nios_sdk.grid._grid_threatprotection import GridThreatprotectionResource
    from ibx_nios_sdk.grid._grid_x509certificate import GridX509certificateResource
    from ibx_nios_sdk.grid._license_gridwide import LicenseGridwideResource
    from ibx_nios_sdk.grid._mastergrid import MastergridResource
    from ibx_nios_sdk.grid._member import MemberResource
    from ibx_nios_sdk.grid._member_dhcpproperties import MemberDhcppropertiesResource
    from ibx_nios_sdk.grid._member_dns import MemberDnsResource
    from ibx_nios_sdk.grid._member_filedistribution import MemberFiledistributionResource
    from ibx_nios_sdk.grid._member_license import MemberLicenseResource
    from ibx_nios_sdk.grid._member_parentalcontrol import MemberParentalcontrolResource
    from ibx_nios_sdk.grid._member_threatinsight import MemberThreatinsightResource
    from ibx_nios_sdk.grid._member_threatprotection import MemberThreatprotectionResource
    from ibx_nios_sdk.grid._membercloudsync import MembercloudsyncResource
    from ibx_nios_sdk.grid._memberdfp import MemberdfpResource
    from ibx_nios_sdk.grid._natgroup import NatgroupResource
    from ibx_nios_sdk.grid._restartservicestatus import RestartservicestatusResource
    from ibx_nios_sdk.grid._upgradegroup import UpgradegroupResource
    from ibx_nios_sdk.grid._upgradeschedule import UpgradescheduleResource
    from ibx_nios_sdk.grid._upgradestatus import UpgradestatusResource


class GridService:
    """Entry point for NIOS Grid resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise GridService with an authenticated HTTP client."""
        self._client = client

    # ------------------------------------------------------------------ Task 2
    @cached_property
    def grid(self) -> GridResource:
        """Entry point for NIOS Grid object resources."""
        from ibx_nios_sdk.grid._grid import GridResource

        return GridResource(self._client)

    @cached_property
    def grid_dhcpproperties(self) -> GridDhcppropertiesResource:
        """Entry point for NIOS Grid-level DHCP property resources."""
        from ibx_nios_sdk.grid._grid_dhcpproperties import GridDhcppropertiesResource

        return GridDhcppropertiesResource(self._client)

    @cached_property
    def grid_dns(self) -> GridDnsResource:
        """Entry point for NIOS Grid-level DNS property resources."""
        from ibx_nios_sdk.grid._grid_dns import GridDnsResource

        return GridDnsResource(self._client)

    @cached_property
    def grid_filedistribution(self) -> GridFiledistributionResource:
        """Entry point for NIOS Grid file distribution resources."""
        from ibx_nios_sdk.grid._grid_filedistribution import GridFiledistributionResource

        return GridFiledistributionResource(self._client)

    @cached_property
    def grid_threatprotection(self) -> GridThreatprotectionResource:
        """Entry point for NIOS Grid Threat Protection resources."""
        from ibx_nios_sdk.grid._grid_threatprotection import GridThreatprotectionResource

        return GridThreatprotectionResource(self._client)

    @cached_property
    def grid_threatinsight(self) -> GridThreatinsightResource:
        """Entry point for NIOS Grid Threat Insight resources."""
        from ibx_nios_sdk.grid._grid_threatinsight import GridThreatinsightResource

        return GridThreatinsightResource(self._client)

    @cached_property
    def grid_dashboard(self) -> GridDashboardResource:
        """Entry point for NIOS Grid dashboard resources."""
        from ibx_nios_sdk.grid._grid_dashboard import GridDashboardResource

        return GridDashboardResource(self._client)

    # ------------------------------------------------------------------ Task 3
    @cached_property
    def grid_cloudapi(self) -> GridCloudapiResource:
        """Entry point for NIOS Grid Cloud API resources."""
        from ibx_nios_sdk.grid._grid_cloudapi import GridCloudapiResource

        return GridCloudapiResource(self._client)

    @cached_property
    def grid_cloudapi_cloudstatistics(self) -> GridCloudapiCloudstatisticsResource:
        """Entry point for NIOS Grid Cloud API statistics resources."""
        from ibx_nios_sdk.grid._grid_cloudapi_cloudstatistics import (
            GridCloudapiCloudstatisticsResource,
        )

        return GridCloudapiCloudstatisticsResource(self._client)

    @cached_property
    def grid_cloudapi_tenant(self) -> GridCloudapiTenantResource:
        """Entry point for NIOS Grid Cloud API tenant resources."""
        from ibx_nios_sdk.grid._grid_cloudapi_tenant import GridCloudapiTenantResource

        return GridCloudapiTenantResource(self._client)

    @cached_property
    def grid_cloudapi_vm(self) -> GridCloudapiVmResource:
        """Entry point for NIOS Grid Cloud API VM resources."""
        from ibx_nios_sdk.grid._grid_cloudapi_vm import GridCloudapiVmResource

        return GridCloudapiVmResource(self._client)

    @cached_property
    def grid_cloudapi_vmaddress(self) -> GridCloudapiVmaddressResource:
        """Entry point for NIOS Grid Cloud API VM address resources."""
        from ibx_nios_sdk.grid._grid_cloudapi_vmaddress import GridCloudapiVmaddressResource

        return GridCloudapiVmaddressResource(self._client)

    @cached_property
    def grid_member_cloudapi(self) -> GridMemberCloudapiResource:
        """Entry point for NIOS Grid member Cloud API resources."""
        from ibx_nios_sdk.grid._grid_member_cloudapi import GridMemberCloudapiResource

        return GridMemberCloudapiResource(self._client)

    # ------------------------------------------------------------------ Task 4
    @cached_property
    def grid_servicerestart_group(self) -> GridServicerestartGroupResource:
        """Entry point for NIOS Grid service-restart group resources."""
        from ibx_nios_sdk.grid._grid_servicerestart_group import GridServicerestartGroupResource

        return GridServicerestartGroupResource(self._client)

    @cached_property
    def grid_servicerestart_status(self) -> GridServicerestartStatusResource:
        """Entry point for NIOS Grid service restart status resources."""
        from ibx_nios_sdk.grid._grid_servicerestart_status import GridServicerestartStatusResource

        return GridServicerestartStatusResource(self._client)

    @cached_property
    def grid_servicerestart_request(self) -> GridServicerestartRequestResource:
        """Entry point for NIOS Grid service restart request resources."""
        from ibx_nios_sdk.grid._grid_servicerestart_request import (
            GridServicerestartRequestResource,
        )

        return GridServicerestartRequestResource(self._client)

    @cached_property
    def grid_servicerestart_group_order(self) -> GridServicerestartGroupOrderResource:
        """Entry point for NIOS Grid service-restart group order resources."""
        from ibx_nios_sdk.grid._grid_servicerestart_group_order import (
            GridServicerestartGroupOrderResource,
        )

        return GridServicerestartGroupOrderResource(self._client)

    @cached_property
    def grid_servicerestart_request_changedobject(
        self,
    ) -> GridServicerestartRequestChangedobjectResource:
        """Entry point for NIOS Grid service restart changed object resources."""
        from ibx_nios_sdk.grid._grid_servicerestart_request_changedobject import (
            GridServicerestartRequestChangedobjectResource,
        )

        return GridServicerestartRequestChangedobjectResource(self._client)

    # ------------------------------------------------------------------ Task 5
    @cached_property
    def member(self) -> MemberResource:
        """Entry point for NIOS Grid member resources."""
        from ibx_nios_sdk.grid._member import MemberResource

        return MemberResource(self._client)

    @cached_property
    def member_dhcpproperties(self) -> MemberDhcppropertiesResource:
        """Entry point for NIOS member-level DHCP property resources."""
        from ibx_nios_sdk.grid._member_dhcpproperties import MemberDhcppropertiesResource

        return MemberDhcppropertiesResource(self._client)

    @cached_property
    def member_dns(self) -> MemberDnsResource:
        """Entry point for NIOS member-level DNS property resources."""
        from ibx_nios_sdk.grid._member_dns import MemberDnsResource

        return MemberDnsResource(self._client)

    @cached_property
    def member_filedistribution(self) -> MemberFiledistributionResource:
        """Entry point for NIOS member file distribution resources."""
        from ibx_nios_sdk.grid._member_filedistribution import MemberFiledistributionResource

        return MemberFiledistributionResource(self._client)

    @cached_property
    def member_license(self) -> MemberLicenseResource:
        """Entry point for NIOS member license resources."""
        from ibx_nios_sdk.grid._member_license import MemberLicenseResource

        return MemberLicenseResource(self._client)

    @cached_property
    def member_threatprotection(self) -> MemberThreatprotectionResource:
        """Entry point for NIOS member Threat Protection resources."""
        from ibx_nios_sdk.grid._member_threatprotection import MemberThreatprotectionResource

        return MemberThreatprotectionResource(self._client)

    @cached_property
    def member_parentalcontrol(self) -> MemberParentalcontrolResource:
        """Entry point for NIOS member parental control resources."""
        from ibx_nios_sdk.grid._member_parentalcontrol import MemberParentalcontrolResource

        return MemberParentalcontrolResource(self._client)

    @cached_property
    def member_threatinsight(self) -> MemberThreatinsightResource:
        """Entry point for NIOS member Threat Insight resources."""
        from ibx_nios_sdk.grid._member_threatinsight import MemberThreatinsightResource

        return MemberThreatinsightResource(self._client)

    @cached_property
    def memberdfp(self) -> MemberdfpResource:
        """Entry point for NIOS member DNS Firewall Policy resources."""
        from ibx_nios_sdk.grid._memberdfp import MemberdfpResource

        return MemberdfpResource(self._client)

    # ------------------------------------------------------------------ Task 7
    @cached_property
    def grid_license_pool(self) -> GridLicensePoolResource:
        """Entry point for NIOS Grid license pool resources."""
        from ibx_nios_sdk.grid._grid_license_pool import GridLicensePoolResource

        return GridLicensePoolResource(self._client)

    @cached_property
    def grid_license_pool_container(self) -> GridLicensePoolContainerResource:
        """Entry point for NIOS Grid license pool container resources."""
        from ibx_nios_sdk.grid._grid_license_pool_container import GridLicensePoolContainerResource

        return GridLicensePoolContainerResource(self._client)

    @cached_property
    def license_gridwide(self) -> LicenseGridwideResource:
        """Entry point for NIOS grid-wide license resources."""
        from ibx_nios_sdk.grid._license_gridwide import LicenseGridwideResource

        return LicenseGridwideResource(self._client)

    @cached_property
    def grid_x509certificate(self) -> GridX509certificateResource:
        """Entry point for NIOS Grid X.509 certificate resources."""
        from ibx_nios_sdk.grid._grid_x509certificate import GridX509certificateResource

        return GridX509certificateResource(self._client)

    # ------------------------------------------------------------------ Task 6
    @cached_property
    def membercloudsync(self) -> MembercloudsyncResource:
        """Entry point for NIOS member cloud sync resources."""
        from ibx_nios_sdk.grid._membercloudsync import MembercloudsyncResource

        return MembercloudsyncResource(self._client)

    @cached_property
    def captiveportal(self) -> CaptiveportalResource:
        """Entry point for NIOS captive portal resources."""
        from ibx_nios_sdk.grid._captiveportal import CaptiveportalResource

        return CaptiveportalResource(self._client)

    @cached_property
    def mastergrid(self) -> MastergridResource:
        """Entry point for NIOS master grid resources."""
        from ibx_nios_sdk.grid._mastergrid import MastergridResource

        return MastergridResource(self._client)

    # ------------------------------------------------------------------ Task 8
    @cached_property
    def upgradegroup(self) -> UpgradegroupResource:
        """Entry point for NIOS upgrade group resources."""
        from ibx_nios_sdk.grid._upgradegroup import UpgradegroupResource

        return UpgradegroupResource(self._client)

    @cached_property
    def upgradeschedule(self) -> UpgradescheduleResource:
        """Entry point for NIOS upgrade schedule resources."""
        from ibx_nios_sdk.grid._upgradeschedule import UpgradescheduleResource

        return UpgradescheduleResource(self._client)

    @cached_property
    def upgradestatus(self) -> UpgradestatusResource:
        """Entry point for NIOS upgrade status resources."""
        from ibx_nios_sdk.grid._upgradestatus import UpgradestatusResource

        return UpgradestatusResource(self._client)

    @cached_property
    def distributionschedule(self) -> DistributionscheduleResource:
        """Entry point for NIOS software distribution schedule resources."""
        from ibx_nios_sdk.grid._distributionschedule import DistributionscheduleResource

        return DistributionscheduleResource(self._client)

    @cached_property
    def gmcgroup(self) -> GmcgroupResource:
        """Entry point for NIOS Grid member cloud group resources."""
        from ibx_nios_sdk.grid._gmcgroup import GmcgroupResource

        return GmcgroupResource(self._client)

    @cached_property
    def gmcschedule(self) -> GmcscheduleResource:
        """Entry point for NIOS Grid member cloud schedule resources."""
        from ibx_nios_sdk.grid._gmcschedule import GmcscheduleResource

        return GmcscheduleResource(self._client)

    # ------------------------------------------------------------------ Task 9
    @cached_property
    def grid_maxminddbinfo(self) -> GridMaxminddbinfoResource:
        """Entry point for NIOS Grid MaxMind database info resources."""
        from ibx_nios_sdk.grid._grid_maxminddbinfo import GridMaxminddbinfoResource

        return GridMaxminddbinfoResource(self._client)

    @cached_property
    def natgroup(self) -> NatgroupResource:
        """Entry point for NIOS NAT group resources."""
        from ibx_nios_sdk.grid._natgroup import NatgroupResource

        return NatgroupResource(self._client)

    @cached_property
    def restartservicestatus(self) -> RestartservicestatusResource:
        """Entry point for NIOS restart service status resources."""
        from ibx_nios_sdk.grid._restartservicestatus import RestartservicestatusResource

        return RestartservicestatusResource(self._client)

    @cached_property
    def extensibleattributedef(self) -> ExtensibleattributedefResource:
        """Entry point for NIOS extensible attribute definition resources."""
        from ibx_nios_sdk.grid._extensibleattributedef import ExtensibleattributedefResource

        return ExtensibleattributedefResource(self._client)
