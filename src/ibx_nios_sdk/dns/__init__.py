# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DNS domain - NIOS DNS objects (zones, records, views, nsgroups)."""

from __future__ import annotations

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
from ibx_nios_sdk.dns._service import DnsService
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

__all__ = [
    "AllnsgroupResource",
    "AllrecordsResource",
    "DdnsPrincipalclusterResource",
    "DdnsPrincipalclusterGroupResource",
    "Dns64groupResource",
    "DnsService",
    "OrderedresponsepolicyzonesResource",
    "RecordnamepolicyResource",
    "ZoneAuthDiscrepancyResource",
    "NsgroupResource",
    "NsgroupDelegationResource",
    "NsgroupForwardingmemberResource",
    "NsgroupForwardstubserverResource",
    "NsgroupStubmemberResource",
    "RecordAResource",
    "SharedrecordAResource",
    "SharedrecordAaaaResource",
    "SharedrecordCnameResource",
    "SharedrecordMxResource",
    "SharedrecordSrvResource",
    "SharedrecordTxtResource",
    "SharedrecordgroupResource",
    "RecordAaaaResource",
    "RecordAliasResource",
    "RecordCaaResource",
    "RecordCnameResource",
    "RecordDhcidResource",
    "RecordDnameResource",
    "RecordDnskeyResource",
    "RecordDsResource",
    "RecordDtclbdnResource",
    "RecordHostResource",
    "RecordHostIpv4addrResource",
    "RecordHostIpv6addrResource",
    "RecordHttpsResource",
    "RecordMxResource",
    "RecordNaptrResource",
    "RecordNsResource",
    "RecordNsecResource",
    "RecordNsec3Resource",
    "RecordNsec3paramResource",
    "RecordPtrResource",
    "RecordRrsigResource",
    "RecordSrvResource",
    "RecordSvcbResource",
    "RecordTlsaResource",
    "RecordTxtResource",
    "RecordUnknownResource",
    "ViewResource",
    "ZoneAuthResource",
    "ZoneDelegatedResource",
    "ZoneForwardResource",
    "ZoneRpResource",
    "ZoneStubResource",
]
