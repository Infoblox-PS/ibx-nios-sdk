# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MiscService - entry point for miscellaneous resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.misc._allendpoints import AllendpointsResource
    from ibx_nios_sdk.misc._bfdtemplate import BfdtemplateResource
    from ibx_nios_sdk.misc._capacityreport import CapacityreportResource
    from ibx_nios_sdk.misc._csvimporttask import CsvimporttaskResource
    from ibx_nios_sdk.misc._datacollectioncluster import DatacollectionclusterResource
    from ibx_nios_sdk.misc._db_objects import DbObjectsResource
    from ibx_nios_sdk.misc._dbsnapshot import DbsnapshotResource
    from ibx_nios_sdk.misc._deleted_objects import DeletedObjectsResource
    from ibx_nios_sdk.misc._dxl_endpoint import DxlEndpointResource
    from ibx_nios_sdk.misc._fileop import FileopResource
    from ibx_nios_sdk.misc._kerberoskey import KerberoskeyResource
    from ibx_nios_sdk.misc._outbound_cloudclient import OutboundCloudclientResource
    from ibx_nios_sdk.misc._pxgrid_endpoint import PxgridEndpointResource
    from ibx_nios_sdk.misc._request import RequestResource
    from ibx_nios_sdk.misc._ruleset import RulesetResource
    from ibx_nios_sdk.misc._scavengingtask import ScavengingtaskResource
    from ibx_nios_sdk.misc._scheduledtask import ScheduledtaskResource
    from ibx_nios_sdk.misc._search import SearchResource
    from ibx_nios_sdk.misc._syslog_endpoint import SyslogEndpointResource
    from ibx_nios_sdk.misc._taxii import TaxiiResource
    from ibx_nios_sdk.misc._tftpfiledir import TftpfiledirResource


class MiscService:
    """Entry point for NIOS miscellaneous resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise MiscService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def allendpoints(self) -> AllendpointsResource:
        """Entry point for NIOS all-endpoint aggregate resources."""
        from ibx_nios_sdk.misc._allendpoints import AllendpointsResource

        return AllendpointsResource(self._client)

    @cached_property
    def bfdtemplate(self) -> BfdtemplateResource:
        """Entry point for NIOS BFD template resources."""
        from ibx_nios_sdk.misc._bfdtemplate import BfdtemplateResource

        return BfdtemplateResource(self._client)

    @cached_property
    def capacityreport(self) -> CapacityreportResource:
        """Entry point for NIOS capacity report resources."""
        from ibx_nios_sdk.misc._capacityreport import CapacityreportResource

        return CapacityreportResource(self._client)

    @cached_property
    def csvimporttask(self) -> CsvimporttaskResource:
        """Entry point for NIOS CSV import task resources."""
        from ibx_nios_sdk.misc._csvimporttask import CsvimporttaskResource

        return CsvimporttaskResource(self._client)

    @cached_property
    def datacollectioncluster(self) -> DatacollectionclusterResource:
        """Entry point for NIOS data collection cluster resources."""
        from ibx_nios_sdk.misc._datacollectioncluster import DatacollectionclusterResource

        return DatacollectionclusterResource(self._client)

    @cached_property
    def db_objects(self) -> DbObjectsResource:
        """Entry point for NIOS database object resources."""
        from ibx_nios_sdk.misc._db_objects import DbObjectsResource

        return DbObjectsResource(self._client)

    @cached_property
    def dbsnapshot(self) -> DbsnapshotResource:
        """Entry point for NIOS database snapshot resources."""
        from ibx_nios_sdk.misc._dbsnapshot import DbsnapshotResource

        return DbsnapshotResource(self._client)

    @cached_property
    def deleted_objects(self) -> DeletedObjectsResource:
        """Entry point for NIOS deleted object resources."""
        from ibx_nios_sdk.misc._deleted_objects import DeletedObjectsResource

        return DeletedObjectsResource(self._client)

    @cached_property
    def dxl_endpoint(self) -> DxlEndpointResource:
        """Entry point for NIOS DXL endpoint resources."""
        from ibx_nios_sdk.misc._dxl_endpoint import DxlEndpointResource

        return DxlEndpointResource(self._client)

    @cached_property
    def fileop(self) -> FileopResource:
        """Entry point for NIOS fileop function-only resources."""
        from ibx_nios_sdk.misc._fileop import FileopResource

        return FileopResource(self._client)

    @cached_property
    def kerberoskey(self) -> KerberoskeyResource:
        """Entry point for NIOS Kerberos key resources."""
        from ibx_nios_sdk.misc._kerberoskey import KerberoskeyResource

        return KerberoskeyResource(self._client)

    @cached_property
    def outbound_cloudclient(self) -> OutboundCloudclientResource:
        """Entry point for NIOS outbound cloud client resources."""
        from ibx_nios_sdk.misc._outbound_cloudclient import OutboundCloudclientResource

        return OutboundCloudclientResource(self._client)

    @cached_property
    def pxgrid_endpoint(self) -> PxgridEndpointResource:
        """Entry point for NIOS pxGrid endpoint resources."""
        from ibx_nios_sdk.misc._pxgrid_endpoint import PxgridEndpointResource

        return PxgridEndpointResource(self._client)

    @cached_property
    def request(self) -> RequestResource:
        """Entry point for NIOS generic multi-request endpoint."""
        from ibx_nios_sdk.misc._request import RequestResource

        return RequestResource(self._client)

    @cached_property
    def ruleset(self) -> RulesetResource:
        """Entry point for NIOS ruleset resources."""
        from ibx_nios_sdk.misc._ruleset import RulesetResource

        return RulesetResource(self._client)

    @cached_property
    def scavengingtask(self) -> ScavengingtaskResource:
        """Entry point for NIOS DNS scavenging task resources."""
        from ibx_nios_sdk.misc._scavengingtask import ScavengingtaskResource

        return ScavengingtaskResource(self._client)

    @cached_property
    def scheduledtask(self) -> ScheduledtaskResource:
        """Entry point for NIOS scheduled task resources."""
        from ibx_nios_sdk.misc._scheduledtask import ScheduledtaskResource

        return ScheduledtaskResource(self._client)

    @cached_property
    def search(self) -> SearchResource:
        """Entry point for NIOS global search function-only resources."""
        from ibx_nios_sdk.misc._search import SearchResource

        return SearchResource(self._client)

    @cached_property
    def syslog_endpoint(self) -> SyslogEndpointResource:
        """Entry point for NIOS syslog endpoint resources."""
        from ibx_nios_sdk.misc._syslog_endpoint import SyslogEndpointResource

        return SyslogEndpointResource(self._client)

    @cached_property
    def taxii(self) -> TaxiiResource:
        """Entry point for NIOS TAXII configuration resources."""
        from ibx_nios_sdk.misc._taxii import TaxiiResource

        return TaxiiResource(self._client)

    @cached_property
    def tftpfiledir(self) -> TftpfiledirResource:
        """Entry point for NIOS TFTP file directory resources."""
        from ibx_nios_sdk.misc._tftpfiledir import TftpfiledirResource

        return TftpfiledirResource(self._client)
