# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DNS domain pydantic models."""

from __future__ import annotations

from ibx_nios_sdk.dns.models.allnsgroup import Allnsgroup
from ibx_nios_sdk.dns.models.allrecords import Allrecords
from ibx_nios_sdk.dns.models.ddns_principalcluster import DdnsPrincipalcluster
from ibx_nios_sdk.dns.models.ddns_principalcluster_group import DdnsPrincipalclusterGroup
from ibx_nios_sdk.dns.models.dns64group import Dns64group
from ibx_nios_sdk.dns.models.nsgroup import Nsgroup
from ibx_nios_sdk.dns.models.nsgroup_delegation import NsgroupDelegation
from ibx_nios_sdk.dns.models.nsgroup_forwardingmember import NsgroupForwardingmember
from ibx_nios_sdk.dns.models.nsgroup_forwardstubserver import NsgroupForwardstubserver
from ibx_nios_sdk.dns.models.nsgroup_stubmember import NsgroupStubmember
from ibx_nios_sdk.dns.models.orderedresponsepolicyzones import Orderedresponsepolicyzones
from ibx_nios_sdk.dns.models.record_a import RecordA
from ibx_nios_sdk.dns.models.record_aaaa import RecordAaaa
from ibx_nios_sdk.dns.models.record_alias import RecordAlias
from ibx_nios_sdk.dns.models.record_caa import RecordCaa
from ibx_nios_sdk.dns.models.record_cname import RecordCname
from ibx_nios_sdk.dns.models.record_dhcid import RecordDhcid
from ibx_nios_sdk.dns.models.record_dname import RecordDname
from ibx_nios_sdk.dns.models.record_dnskey import RecordDnskey
from ibx_nios_sdk.dns.models.record_ds import RecordDs
from ibx_nios_sdk.dns.models.record_dtclbdn import RecordDtclbdn
from ibx_nios_sdk.dns.models.record_host import RecordHost
from ibx_nios_sdk.dns.models.record_host_ipv4addr import RecordHostIpv4addr
from ibx_nios_sdk.dns.models.record_host_ipv6addr import RecordHostIpv6addr
from ibx_nios_sdk.dns.models.record_https import RecordHttps
from ibx_nios_sdk.dns.models.record_mx import RecordMx
from ibx_nios_sdk.dns.models.record_naptr import RecordNaptr
from ibx_nios_sdk.dns.models.record_ns import RecordNs
from ibx_nios_sdk.dns.models.record_nsec import RecordNsec
from ibx_nios_sdk.dns.models.record_nsec3 import RecordNsec3
from ibx_nios_sdk.dns.models.record_nsec3param import RecordNsec3param
from ibx_nios_sdk.dns.models.record_ptr import RecordPtr
from ibx_nios_sdk.dns.models.record_rrsig import RecordRrsig
from ibx_nios_sdk.dns.models.record_srv import RecordSrv
from ibx_nios_sdk.dns.models.record_svcb import RecordSvcb
from ibx_nios_sdk.dns.models.record_tlsa import RecordTlsa
from ibx_nios_sdk.dns.models.record_txt import RecordTxt
from ibx_nios_sdk.dns.models.record_unknown import RecordUnknown
from ibx_nios_sdk.dns.models.recordnamepolicy import Recordnamepolicy
from ibx_nios_sdk.dns.models.sharedrecord_a import SharedrecordA
from ibx_nios_sdk.dns.models.sharedrecord_aaaa import SharedrecordAaaa
from ibx_nios_sdk.dns.models.sharedrecord_cname import SharedrecordCname
from ibx_nios_sdk.dns.models.sharedrecord_mx import SharedrecordMx
from ibx_nios_sdk.dns.models.sharedrecord_srv import SharedrecordSrv
from ibx_nios_sdk.dns.models.sharedrecord_txt import SharedrecordTxt
from ibx_nios_sdk.dns.models.sharedrecordgroup import Sharedrecordgroup
from ibx_nios_sdk.dns.models.view import View
from ibx_nios_sdk.dns.models.zone_auth import ZoneAuth
from ibx_nios_sdk.dns.models.zone_auth_discrepancy import ZoneAuthDiscrepancy
from ibx_nios_sdk.dns.models.zone_delegated import ZoneDelegated
from ibx_nios_sdk.dns.models.zone_forward import ZoneForward
from ibx_nios_sdk.dns.models.zone_rp import ZoneRp
from ibx_nios_sdk.dns.models.zone_stub import ZoneStub

__all__ = [
    "Allnsgroup",
    "Allrecords",
    "DdnsPrincipalcluster",
    "DdnsPrincipalclusterGroup",
    "Dns64group",
    "Orderedresponsepolicyzones",
    "Recordnamepolicy",
    "ZoneAuthDiscrepancy",
    "Nsgroup",
    "NsgroupDelegation",
    "NsgroupForwardingmember",
    "NsgroupForwardstubserver",
    "NsgroupStubmember",
    "RecordA",
    "SharedrecordA",
    "SharedrecordAaaa",
    "SharedrecordCname",
    "SharedrecordMx",
    "SharedrecordSrv",
    "SharedrecordTxt",
    "Sharedrecordgroup",
    "RecordAaaa",
    "RecordAlias",
    "RecordCaa",
    "RecordCname",
    "RecordDhcid",
    "RecordDname",
    "RecordDnskey",
    "RecordDs",
    "RecordDtclbdn",
    "RecordHost",
    "RecordHostIpv4addr",
    "RecordHostIpv6addr",
    "RecordHttps",
    "RecordMx",
    "RecordNaptr",
    "RecordNs",
    "RecordNsec",
    "RecordNsec3",
    "RecordNsec3param",
    "RecordPtr",
    "RecordRrsig",
    "RecordSrv",
    "RecordSvcb",
    "RecordTlsa",
    "RecordTxt",
    "RecordUnknown",
    "View",
    "ZoneAuth",
    "ZoneDelegated",
    "ZoneForward",
    "ZoneRp",
    "ZoneStub",
]
