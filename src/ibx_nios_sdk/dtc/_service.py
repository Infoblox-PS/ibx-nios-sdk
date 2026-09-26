# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcService - entry point for DTC (Dynamic Traffic Control) resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.dtc._dtc import DtcResource
    from ibx_nios_sdk.dtc._dtc_allrecords import DtcAllrecordsResource
    from ibx_nios_sdk.dtc._dtc_certificate import DtcCertificateResource
    from ibx_nios_sdk.dtc._dtc_lbdn import DtcLbdnResource
    from ibx_nios_sdk.dtc._dtc_monitor import DtcMonitorResource
    from ibx_nios_sdk.dtc._dtc_monitor_http import DtcMonitorHttpResource
    from ibx_nios_sdk.dtc._dtc_monitor_icmp import DtcMonitorIcmpResource
    from ibx_nios_sdk.dtc._dtc_monitor_pdp import DtcMonitorPdpResource
    from ibx_nios_sdk.dtc._dtc_monitor_sip import DtcMonitorSipResource
    from ibx_nios_sdk.dtc._dtc_monitor_snmp import DtcMonitorSnmpResource
    from ibx_nios_sdk.dtc._dtc_monitor_tcp import DtcMonitorTcpResource
    from ibx_nios_sdk.dtc._dtc_object import DtcObjectResource
    from ibx_nios_sdk.dtc._dtc_pool import DtcPoolResource
    from ibx_nios_sdk.dtc._dtc_record_a import DtcRecordAResource
    from ibx_nios_sdk.dtc._dtc_record_aaaa import DtcRecordAaaaResource
    from ibx_nios_sdk.dtc._dtc_record_cname import DtcRecordCnameResource
    from ibx_nios_sdk.dtc._dtc_record_naptr import DtcRecordNaptrResource
    from ibx_nios_sdk.dtc._dtc_record_srv import DtcRecordSrvResource
    from ibx_nios_sdk.dtc._dtc_server import DtcServerResource
    from ibx_nios_sdk.dtc._dtc_topology import DtcTopologyResource
    from ibx_nios_sdk.dtc._dtc_topology_label import DtcTopologyLabelResource
    from ibx_nios_sdk.dtc._dtc_topology_rule import DtcTopologyRuleResource


class DtcService:
    """Entry point for NIOS DTC resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise DtcService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def dtc(self) -> DtcResource:
        """Entry point for NIOS DTC global configuration resources."""
        from ibx_nios_sdk.dtc._dtc import DtcResource

        return DtcResource(self._client)

    @cached_property
    def server(self) -> DtcServerResource:
        """Entry point for NIOS DTC server resources."""
        from ibx_nios_sdk.dtc._dtc_server import DtcServerResource

        return DtcServerResource(self._client)

    @cached_property
    def pool(self) -> DtcPoolResource:
        """Entry point for NIOS DTC server pool resources."""
        from ibx_nios_sdk.dtc._dtc_pool import DtcPoolResource

        return DtcPoolResource(self._client)

    @cached_property
    def lbdn(self) -> DtcLbdnResource:
        """Entry point for NIOS DTC LBDN resources."""
        from ibx_nios_sdk.dtc._dtc_lbdn import DtcLbdnResource

        return DtcLbdnResource(self._client)

    @cached_property
    def topology(self) -> DtcTopologyResource:
        """Entry point for NIOS DTC topology resources."""
        from ibx_nios_sdk.dtc._dtc_topology import DtcTopologyResource

        return DtcTopologyResource(self._client)

    @cached_property
    def topology_rule(self) -> DtcTopologyRuleResource:
        """Entry point for NIOS DTC topology rule resources."""
        from ibx_nios_sdk.dtc._dtc_topology_rule import DtcTopologyRuleResource

        return DtcTopologyRuleResource(self._client)

    @cached_property
    def topology_label(self) -> DtcTopologyLabelResource:
        """Entry point for NIOS DTC topology label resources."""
        from ibx_nios_sdk.dtc._dtc_topology_label import DtcTopologyLabelResource

        return DtcTopologyLabelResource(self._client)

    @cached_property
    def certificate(self) -> DtcCertificateResource:
        """Entry point for NIOS DTC certificate resources."""
        from ibx_nios_sdk.dtc._dtc_certificate import DtcCertificateResource

        return DtcCertificateResource(self._client)

    @cached_property
    def object(self) -> DtcObjectResource:
        """Entry point for NIOS DTC object resources."""
        from ibx_nios_sdk.dtc._dtc_object import DtcObjectResource

        return DtcObjectResource(self._client)

    @cached_property
    def allrecords(self) -> DtcAllrecordsResource:
        """Entry point for NIOS DTC all-records aggregate resources."""
        from ibx_nios_sdk.dtc._dtc_allrecords import DtcAllrecordsResource

        return DtcAllrecordsResource(self._client)

    @cached_property
    def monitor(self) -> DtcMonitorResource:
        """Entry point for NIOS DTC health monitor resources."""
        from ibx_nios_sdk.dtc._dtc_monitor import DtcMonitorResource

        return DtcMonitorResource(self._client)

    @cached_property
    def monitor_http(self) -> DtcMonitorHttpResource:
        """Entry point for NIOS DTC HTTP health monitor resources."""
        from ibx_nios_sdk.dtc._dtc_monitor_http import DtcMonitorHttpResource

        return DtcMonitorHttpResource(self._client)

    @cached_property
    def monitor_icmp(self) -> DtcMonitorIcmpResource:
        """Entry point for NIOS DTC ICMP health monitor resources."""
        from ibx_nios_sdk.dtc._dtc_monitor_icmp import DtcMonitorIcmpResource

        return DtcMonitorIcmpResource(self._client)

    @cached_property
    def monitor_pdp(self) -> DtcMonitorPdpResource:
        """Entry point for NIOS DTC PDP health monitor resources."""
        from ibx_nios_sdk.dtc._dtc_monitor_pdp import DtcMonitorPdpResource

        return DtcMonitorPdpResource(self._client)

    @cached_property
    def monitor_sip(self) -> DtcMonitorSipResource:
        """Entry point for NIOS DTC SIP health monitor resources."""
        from ibx_nios_sdk.dtc._dtc_monitor_sip import DtcMonitorSipResource

        return DtcMonitorSipResource(self._client)

    @cached_property
    def monitor_snmp(self) -> DtcMonitorSnmpResource:
        """Entry point for NIOS DTC SNMP health monitor resources."""
        from ibx_nios_sdk.dtc._dtc_monitor_snmp import DtcMonitorSnmpResource

        return DtcMonitorSnmpResource(self._client)

    @cached_property
    def monitor_tcp(self) -> DtcMonitorTcpResource:
        """Entry point for NIOS DTC TCP health monitor resources."""
        from ibx_nios_sdk.dtc._dtc_monitor_tcp import DtcMonitorTcpResource

        return DtcMonitorTcpResource(self._client)

    @cached_property
    def record_a(self) -> DtcRecordAResource:
        """Entry point for NIOS DTC A record resources."""
        from ibx_nios_sdk.dtc._dtc_record_a import DtcRecordAResource

        return DtcRecordAResource(self._client)

    @cached_property
    def record_aaaa(self) -> DtcRecordAaaaResource:
        """Entry point for NIOS DTC AAAA record resources."""
        from ibx_nios_sdk.dtc._dtc_record_aaaa import DtcRecordAaaaResource

        return DtcRecordAaaaResource(self._client)

    @cached_property
    def record_cname(self) -> DtcRecordCnameResource:
        """Entry point for NIOS DTC CNAME record resources."""
        from ibx_nios_sdk.dtc._dtc_record_cname import DtcRecordCnameResource

        return DtcRecordCnameResource(self._client)

    @cached_property
    def record_naptr(self) -> DtcRecordNaptrResource:
        """Entry point for NIOS DTC NAPTR record resources."""
        from ibx_nios_sdk.dtc._dtc_record_naptr import DtcRecordNaptrResource

        return DtcRecordNaptrResource(self._client)

    @cached_property
    def record_srv(self) -> DtcRecordSrvResource:
        """Entry point for NIOS DTC SRV record resources."""
        from ibx_nios_sdk.dtc._dtc_record_srv import DtcRecordSrvResource

        return DtcRecordSrvResource(self._client)
