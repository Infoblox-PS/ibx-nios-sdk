# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DnsService - entry point for DNS resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.dns._allnsgroup import AllnsgroupResource
    from ibx_nios_sdk.dns._allrecords import AllrecordsResource
    from ibx_nios_sdk.dns._ddns_principalcluster import DdnsPrincipalclusterResource
    from ibx_nios_sdk.dns._ddns_principalcluster_group import DdnsPrincipalclusterGroupResource
    from ibx_nios_sdk.dns._dns64group import Dns64groupResource
    from ibx_nios_sdk.dns._nsgroup import NsgroupResource
    from ibx_nios_sdk.dns._nsgroup_delegation import NsgroupDelegationResource
    from ibx_nios_sdk.dns._nsgroup_forwardingmember import NsgroupForwardingmemberResource
    from ibx_nios_sdk.dns._nsgroup_forwardstubserver import NsgroupForwardstubserverResource
    from ibx_nios_sdk.dns._nsgroup_stubmember import NsgroupStubmemberResource
    from ibx_nios_sdk.dns._orderedresponsepolicyzones import OrderedresponsepolicyzonesResource
    from ibx_nios_sdk.dns._record_a import RecordAResource
    from ibx_nios_sdk.dns._record_aaaa import RecordAaaaResource
    from ibx_nios_sdk.dns._record_alias import RecordAliasResource
    from ibx_nios_sdk.dns._record_caa import RecordCaaResource
    from ibx_nios_sdk.dns._record_cname import RecordCnameResource
    from ibx_nios_sdk.dns._record_dhcid import RecordDhcidResource
    from ibx_nios_sdk.dns._record_dname import RecordDnameResource
    from ibx_nios_sdk.dns._record_dnskey import RecordDnskeyResource
    from ibx_nios_sdk.dns._record_ds import RecordDsResource
    from ibx_nios_sdk.dns._record_dtclbdn import RecordDtclbdnResource
    from ibx_nios_sdk.dns._record_host import RecordHostResource
    from ibx_nios_sdk.dns._record_host_ipv4addr import RecordHostIpv4addrResource
    from ibx_nios_sdk.dns._record_host_ipv6addr import RecordHostIpv6addrResource
    from ibx_nios_sdk.dns._record_https import RecordHttpsResource
    from ibx_nios_sdk.dns._record_mx import RecordMxResource
    from ibx_nios_sdk.dns._record_naptr import RecordNaptrResource
    from ibx_nios_sdk.dns._record_ns import RecordNsResource
    from ibx_nios_sdk.dns._record_nsec import RecordNsecResource
    from ibx_nios_sdk.dns._record_nsec3 import RecordNsec3Resource
    from ibx_nios_sdk.dns._record_nsec3param import RecordNsec3paramResource
    from ibx_nios_sdk.dns._record_ptr import RecordPtrResource
    from ibx_nios_sdk.dns._record_rrsig import RecordRrsigResource
    from ibx_nios_sdk.dns._record_srv import RecordSrvResource
    from ibx_nios_sdk.dns._record_svcb import RecordSvcbResource
    from ibx_nios_sdk.dns._record_tlsa import RecordTlsaResource
    from ibx_nios_sdk.dns._record_txt import RecordTxtResource
    from ibx_nios_sdk.dns._record_unknown import RecordUnknownResource
    from ibx_nios_sdk.dns._recordnamepolicy import RecordnamepolicyResource
    from ibx_nios_sdk.dns._sharedrecord_a import SharedrecordAResource
    from ibx_nios_sdk.dns._sharedrecord_aaaa import SharedrecordAaaaResource
    from ibx_nios_sdk.dns._sharedrecord_cname import SharedrecordCnameResource
    from ibx_nios_sdk.dns._sharedrecord_mx import SharedrecordMxResource
    from ibx_nios_sdk.dns._sharedrecord_srv import SharedrecordSrvResource
    from ibx_nios_sdk.dns._sharedrecord_txt import SharedrecordTxtResource
    from ibx_nios_sdk.dns._sharedrecordgroup import SharedrecordgroupResource
    from ibx_nios_sdk.dns._view import ViewResource
    from ibx_nios_sdk.dns._zone_auth import ZoneAuthResource
    from ibx_nios_sdk.dns._zone_auth_discrepancy import ZoneAuthDiscrepancyResource
    from ibx_nios_sdk.dns._zone_delegated import ZoneDelegatedResource
    from ibx_nios_sdk.dns._zone_forward import ZoneForwardResource
    from ibx_nios_sdk.dns._zone_rp import ZoneRpResource
    from ibx_nios_sdk.dns._zone_stub import ZoneStubResource


class DnsService:
    """Entry point for NIOS DNS resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise DnsService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def view(self) -> ViewResource:
        """Entry point for NIOS DNS view resources."""
        from ibx_nios_sdk.dns._view import ViewResource

        return ViewResource(self._client)

    @cached_property
    def zone_auth(self) -> ZoneAuthResource:
        """Entry point for NIOS authoritative DNS zone resources."""
        from ibx_nios_sdk.dns._zone_auth import ZoneAuthResource

        return ZoneAuthResource(self._client)

    @cached_property
    def zone_forward(self) -> ZoneForwardResource:
        """Entry point for NIOS forward DNS zone resources."""
        from ibx_nios_sdk.dns._zone_forward import ZoneForwardResource

        return ZoneForwardResource(self._client)

    @cached_property
    def zone_delegated(self) -> ZoneDelegatedResource:
        """Entry point for NIOS delegated DNS zone resources."""
        from ibx_nios_sdk.dns._zone_delegated import ZoneDelegatedResource

        return ZoneDelegatedResource(self._client)

    @cached_property
    def zone_stub(self) -> ZoneStubResource:
        """Entry point for NIOS stub DNS zone resources."""
        from ibx_nios_sdk.dns._zone_stub import ZoneStubResource

        return ZoneStubResource(self._client)

    @cached_property
    def zone_rp(self) -> ZoneRpResource:
        """Entry point for NIOS DNS response policy zone (RPZ) resources."""
        from ibx_nios_sdk.dns._zone_rp import ZoneRpResource

        return ZoneRpResource(self._client)

    @cached_property
    def record_a(self) -> RecordAResource:
        """Entry point for NIOS DNS A record resources."""
        from ibx_nios_sdk.dns._record_a import RecordAResource

        return RecordAResource(self._client)

    @cached_property
    def record_aaaa(self) -> RecordAaaaResource:
        """Entry point for NIOS DNS AAAA record resources."""
        from ibx_nios_sdk.dns._record_aaaa import RecordAaaaResource

        return RecordAaaaResource(self._client)

    @cached_property
    def record_cname(self) -> RecordCnameResource:
        """Entry point for NIOS DNS CNAME record resources."""
        from ibx_nios_sdk.dns._record_cname import RecordCnameResource

        return RecordCnameResource(self._client)

    @cached_property
    def record_ptr(self) -> RecordPtrResource:
        """Entry point for NIOS DNS PTR record resources."""
        from ibx_nios_sdk.dns._record_ptr import RecordPtrResource

        return RecordPtrResource(self._client)

    @cached_property
    def record_mx(self) -> RecordMxResource:
        """Entry point for NIOS DNS MX record resources."""
        from ibx_nios_sdk.dns._record_mx import RecordMxResource

        return RecordMxResource(self._client)

    @cached_property
    def record_txt(self) -> RecordTxtResource:
        """Entry point for NIOS DNS TXT record resources."""
        from ibx_nios_sdk.dns._record_txt import RecordTxtResource

        return RecordTxtResource(self._client)

    @cached_property
    def record_srv(self) -> RecordSrvResource:
        """Entry point for NIOS DNS SRV record resources."""
        from ibx_nios_sdk.dns._record_srv import RecordSrvResource

        return RecordSrvResource(self._client)

    @cached_property
    def record_ns(self) -> RecordNsResource:
        """Entry point for NIOS DNS NS record resources."""
        from ibx_nios_sdk.dns._record_ns import RecordNsResource

        return RecordNsResource(self._client)

    @cached_property
    def record_host(self) -> RecordHostResource:
        """Entry point for NIOS DNS host record resources."""
        from ibx_nios_sdk.dns._record_host import RecordHostResource

        return RecordHostResource(self._client)

    @cached_property
    def record_host_ipv4addr(self) -> RecordHostIpv4addrResource:
        """Entry point for NIOS DNS host IPv4 address sub-record resources."""
        from ibx_nios_sdk.dns._record_host_ipv4addr import RecordHostIpv4addrResource

        return RecordHostIpv4addrResource(self._client)

    @cached_property
    def record_host_ipv6addr(self) -> RecordHostIpv6addrResource:
        """Entry point for NIOS DNS host IPv6 address sub-record resources."""
        from ibx_nios_sdk.dns._record_host_ipv6addr import RecordHostIpv6addrResource

        return RecordHostIpv6addrResource(self._client)

    @cached_property
    def record_dnskey(self) -> RecordDnskeyResource:
        """Entry point for NIOS DNS DNSKEY record resources."""
        from ibx_nios_sdk.dns._record_dnskey import RecordDnskeyResource

        return RecordDnskeyResource(self._client)

    @cached_property
    def record_ds(self) -> RecordDsResource:
        """Entry point for NIOS DNS DS record resources."""
        from ibx_nios_sdk.dns._record_ds import RecordDsResource

        return RecordDsResource(self._client)

    @cached_property
    def record_nsec(self) -> RecordNsecResource:
        """Entry point for NIOS DNS NSEC record resources."""
        from ibx_nios_sdk.dns._record_nsec import RecordNsecResource

        return RecordNsecResource(self._client)

    @cached_property
    def record_nsec3(self) -> RecordNsec3Resource:
        """Entry point for NIOS DNS NSEC3 record resources."""
        from ibx_nios_sdk.dns._record_nsec3 import RecordNsec3Resource

        return RecordNsec3Resource(self._client)

    @cached_property
    def record_nsec3param(self) -> RecordNsec3paramResource:
        """Entry point for NIOS DNS NSEC3PARAM record resources."""
        from ibx_nios_sdk.dns._record_nsec3param import RecordNsec3paramResource

        return RecordNsec3paramResource(self._client)

    @cached_property
    def record_rrsig(self) -> RecordRrsigResource:
        """Entry point for NIOS DNS RRSIG record resources."""
        from ibx_nios_sdk.dns._record_rrsig import RecordRrsigResource

        return RecordRrsigResource(self._client)

    @cached_property
    def record_alias(self) -> RecordAliasResource:
        """Entry point for NIOS DNS ALIAS record resources."""
        from ibx_nios_sdk.dns._record_alias import RecordAliasResource

        return RecordAliasResource(self._client)

    @cached_property
    def record_https(self) -> RecordHttpsResource:
        """Entry point for NIOS DNS HTTPS record resources."""
        from ibx_nios_sdk.dns._record_https import RecordHttpsResource

        return RecordHttpsResource(self._client)

    @cached_property
    def record_dname(self) -> RecordDnameResource:
        """Entry point for NIOS DNS DNAME record resources."""
        from ibx_nios_sdk.dns._record_dname import RecordDnameResource

        return RecordDnameResource(self._client)

    @cached_property
    def record_naptr(self) -> RecordNaptrResource:
        """Entry point for NIOS DNS NAPTR record resources."""
        from ibx_nios_sdk.dns._record_naptr import RecordNaptrResource

        return RecordNaptrResource(self._client)

    @cached_property
    def record_tlsa(self) -> RecordTlsaResource:
        """Entry point for NIOS DNS TLSA record resources."""
        from ibx_nios_sdk.dns._record_tlsa import RecordTlsaResource

        return RecordTlsaResource(self._client)

    @cached_property
    def record_caa(self) -> RecordCaaResource:
        """Entry point for NIOS DNS CAA record resources."""
        from ibx_nios_sdk.dns._record_caa import RecordCaaResource

        return RecordCaaResource(self._client)

    @cached_property
    def record_dhcid(self) -> RecordDhcidResource:
        """Entry point for NIOS DNS DHCID record resources."""
        from ibx_nios_sdk.dns._record_dhcid import RecordDhcidResource

        return RecordDhcidResource(self._client)

    @cached_property
    def record_svcb(self) -> RecordSvcbResource:
        """Entry point for NIOS DNS SVCB record resources."""
        from ibx_nios_sdk.dns._record_svcb import RecordSvcbResource

        return RecordSvcbResource(self._client)

    @cached_property
    def record_dtclbdn(self) -> RecordDtclbdnResource:
        """Entry point for NIOS DTC LBDN DNS record resources."""
        from ibx_nios_sdk.dns._record_dtclbdn import RecordDtclbdnResource

        return RecordDtclbdnResource(self._client)

    @cached_property
    def record_unknown(self) -> RecordUnknownResource:
        """Entry point for NIOS DNS unknown/generic record resources."""
        from ibx_nios_sdk.dns._record_unknown import RecordUnknownResource

        return RecordUnknownResource(self._client)

    @cached_property
    def nsgroup(self) -> NsgroupResource:
        """Entry point for NIOS DNS name-server group resources."""
        from ibx_nios_sdk.dns._nsgroup import NsgroupResource

        return NsgroupResource(self._client)

    @cached_property
    def nsgroup_delegation(self) -> NsgroupDelegationResource:
        """Entry point for NIOS DNS delegation name-server group resources."""
        from ibx_nios_sdk.dns._nsgroup_delegation import NsgroupDelegationResource

        return NsgroupDelegationResource(self._client)

    @cached_property
    def nsgroup_forwardingmember(self) -> NsgroupForwardingmemberResource:
        """Entry point for NIOS DNS forwarding member group resources."""
        from ibx_nios_sdk.dns._nsgroup_forwardingmember import NsgroupForwardingmemberResource

        return NsgroupForwardingmemberResource(self._client)

    @cached_property
    def nsgroup_forwardstubserver(self) -> NsgroupForwardstubserverResource:
        """Entry point for NIOS DNS forward/stub server group resources."""
        from ibx_nios_sdk.dns._nsgroup_forwardstubserver import NsgroupForwardstubserverResource

        return NsgroupForwardstubserverResource(self._client)

    @cached_property
    def nsgroup_stubmember(self) -> NsgroupStubmemberResource:
        """Entry point for NIOS DNS stub member group resources."""
        from ibx_nios_sdk.dns._nsgroup_stubmember import NsgroupStubmemberResource

        return NsgroupStubmemberResource(self._client)

    @cached_property
    def allnsgroup(self) -> AllnsgroupResource:
        """Entry point for NIOS DNS all-nameserver-groups aggregate resources."""
        from ibx_nios_sdk.dns._allnsgroup import AllnsgroupResource

        return AllnsgroupResource(self._client)

    @cached_property
    def sharedrecord_a(self) -> SharedrecordAResource:
        """Entry point for NIOS shared DNS A record resources."""
        from ibx_nios_sdk.dns._sharedrecord_a import SharedrecordAResource

        return SharedrecordAResource(self._client)

    @cached_property
    def sharedrecord_aaaa(self) -> SharedrecordAaaaResource:
        """Entry point for NIOS shared DNS AAAA record resources."""
        from ibx_nios_sdk.dns._sharedrecord_aaaa import SharedrecordAaaaResource

        return SharedrecordAaaaResource(self._client)

    @cached_property
    def sharedrecord_cname(self) -> SharedrecordCnameResource:
        """Entry point for NIOS shared DNS CNAME record resources."""
        from ibx_nios_sdk.dns._sharedrecord_cname import SharedrecordCnameResource

        return SharedrecordCnameResource(self._client)

    @cached_property
    def sharedrecord_mx(self) -> SharedrecordMxResource:
        """Entry point for NIOS shared DNS MX record resources."""
        from ibx_nios_sdk.dns._sharedrecord_mx import SharedrecordMxResource

        return SharedrecordMxResource(self._client)

    @cached_property
    def sharedrecord_srv(self) -> SharedrecordSrvResource:
        """Entry point for NIOS shared DNS SRV record resources."""
        from ibx_nios_sdk.dns._sharedrecord_srv import SharedrecordSrvResource

        return SharedrecordSrvResource(self._client)

    @cached_property
    def sharedrecord_txt(self) -> SharedrecordTxtResource:
        """Entry point for NIOS shared DNS TXT record resources."""
        from ibx_nios_sdk.dns._sharedrecord_txt import SharedrecordTxtResource

        return SharedrecordTxtResource(self._client)

    @cached_property
    def sharedrecordgroup(self) -> SharedrecordgroupResource:
        """Entry point for NIOS shared DNS record group resources."""
        from ibx_nios_sdk.dns._sharedrecordgroup import SharedrecordgroupResource

        return SharedrecordgroupResource(self._client)

    @cached_property
    def allrecords(self) -> AllrecordsResource:
        """Entry point for NIOS DNS all-records aggregate resources."""
        from ibx_nios_sdk.dns._allrecords import AllrecordsResource

        return AllrecordsResource(self._client)

    @cached_property
    def recordnamepolicy(self) -> RecordnamepolicyResource:
        """Entry point for NIOS DNS record-name policy resources."""
        from ibx_nios_sdk.dns._recordnamepolicy import RecordnamepolicyResource

        return RecordnamepolicyResource(self._client)

    @cached_property
    def dns64group(self) -> Dns64groupResource:
        """Entry point for NIOS DNS64 synthesis group resources."""
        from ibx_nios_sdk.dns._dns64group import Dns64groupResource

        return Dns64groupResource(self._client)

    @cached_property
    def ddns_principalcluster(self) -> DdnsPrincipalclusterResource:
        """Entry point for NIOS DDNS principal cluster resources."""
        from ibx_nios_sdk.dns._ddns_principalcluster import DdnsPrincipalclusterResource

        return DdnsPrincipalclusterResource(self._client)

    @cached_property
    def ddns_principalcluster_group(self) -> DdnsPrincipalclusterGroupResource:
        """Entry point for NIOS DDNS principal cluster group resources."""
        from ibx_nios_sdk.dns._ddns_principalcluster_group import (
            DdnsPrincipalclusterGroupResource,
        )

        return DdnsPrincipalclusterGroupResource(self._client)

    @cached_property
    def orderedresponsepolicyzones(self) -> OrderedresponsepolicyzonesResource:
        """Entry point for NIOS ordered response policy zones resources."""
        from ibx_nios_sdk.dns._orderedresponsepolicyzones import (
            OrderedresponsepolicyzonesResource,
        )

        return OrderedresponsepolicyzonesResource(self._client)

    @cached_property
    def zone_auth_discrepancy(self) -> ZoneAuthDiscrepancyResource:
        """Entry point for NIOS DNS authoritative zone discrepancy resources."""
        from ibx_nios_sdk.dns._zone_auth_discrepancy import ZoneAuthDiscrepancyResource

        return ZoneAuthDiscrepancyResource(self._client)
