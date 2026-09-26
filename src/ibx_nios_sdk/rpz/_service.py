# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RpzService - entry point for RPZ resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.rpz._allrpzrecords import AllrpzrecordsResource
    from ibx_nios_sdk.rpz._record_rpz_a import RecordRpzAResource
    from ibx_nios_sdk.rpz._record_rpz_a_ipaddress import RecordRpzAIpaddressResource
    from ibx_nios_sdk.rpz._record_rpz_aaaa import RecordRpzAaaaResource
    from ibx_nios_sdk.rpz._record_rpz_aaaa_ipaddress import RecordRpzAaaaIpaddressResource
    from ibx_nios_sdk.rpz._record_rpz_cname import RecordRpzCnameResource
    from ibx_nios_sdk.rpz._record_rpz_cname_clientipaddress import (
        RecordRpzCnameClientipaddressResource,
    )
    from ibx_nios_sdk.rpz._record_rpz_cname_clientipaddressdn import (
        RecordRpzCnameClientipaddressdnResource,
    )
    from ibx_nios_sdk.rpz._record_rpz_cname_ipaddress import RecordRpzCnameIpaddressResource
    from ibx_nios_sdk.rpz._record_rpz_cname_ipaddressdn import RecordRpzCnameIpaddressdnResource
    from ibx_nios_sdk.rpz._record_rpz_https import RecordRpzHttpsResource
    from ibx_nios_sdk.rpz._record_rpz_mx import RecordRpzMxResource
    from ibx_nios_sdk.rpz._record_rpz_naptr import RecordRpzNaptrResource
    from ibx_nios_sdk.rpz._record_rpz_ptr import RecordRpzPtrResource
    from ibx_nios_sdk.rpz._record_rpz_srv import RecordRpzSrvResource
    from ibx_nios_sdk.rpz._record_rpz_svcb import RecordRpzSvcbResource
    from ibx_nios_sdk.rpz._record_rpz_txt import RecordRpzTxtResource


class RpzService:
    """Entry point for NIOS RPZ resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise RpzService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def record_rpz_a(self) -> RecordRpzAResource:
        """Entry point for NIOS RPZ A record resources."""
        from ibx_nios_sdk.rpz._record_rpz_a import RecordRpzAResource

        return RecordRpzAResource(self._client)

    @cached_property
    def record_rpz_aaaa(self) -> RecordRpzAaaaResource:
        """Entry point for NIOS RPZ AAAA record resources."""
        from ibx_nios_sdk.rpz._record_rpz_aaaa import RecordRpzAaaaResource

        return RecordRpzAaaaResource(self._client)

    @cached_property
    def record_rpz_cname(self) -> RecordRpzCnameResource:
        """Entry point for NIOS RPZ CNAME record resources."""
        from ibx_nios_sdk.rpz._record_rpz_cname import RecordRpzCnameResource

        return RecordRpzCnameResource(self._client)

    @cached_property
    def record_rpz_https(self) -> RecordRpzHttpsResource:
        """Entry point for NIOS RPZ HTTPS record resources."""
        from ibx_nios_sdk.rpz._record_rpz_https import RecordRpzHttpsResource

        return RecordRpzHttpsResource(self._client)

    @cached_property
    def record_rpz_mx(self) -> RecordRpzMxResource:
        """Entry point for NIOS RPZ MX record resources."""
        from ibx_nios_sdk.rpz._record_rpz_mx import RecordRpzMxResource

        return RecordRpzMxResource(self._client)

    @cached_property
    def record_rpz_naptr(self) -> RecordRpzNaptrResource:
        """Entry point for NIOS RPZ NAPTR record resources."""
        from ibx_nios_sdk.rpz._record_rpz_naptr import RecordRpzNaptrResource

        return RecordRpzNaptrResource(self._client)

    @cached_property
    def record_rpz_ptr(self) -> RecordRpzPtrResource:
        """Entry point for NIOS RPZ PTR record resources."""
        from ibx_nios_sdk.rpz._record_rpz_ptr import RecordRpzPtrResource

        return RecordRpzPtrResource(self._client)

    @cached_property
    def record_rpz_srv(self) -> RecordRpzSrvResource:
        """Entry point for NIOS RPZ SRV record resources."""
        from ibx_nios_sdk.rpz._record_rpz_srv import RecordRpzSrvResource

        return RecordRpzSrvResource(self._client)

    @cached_property
    def record_rpz_svcb(self) -> RecordRpzSvcbResource:
        """Entry point for NIOS RPZ SVCB record resources."""
        from ibx_nios_sdk.rpz._record_rpz_svcb import RecordRpzSvcbResource

        return RecordRpzSvcbResource(self._client)

    @cached_property
    def record_rpz_txt(self) -> RecordRpzTxtResource:
        """Entry point for NIOS RPZ TXT record resources."""
        from ibx_nios_sdk.rpz._record_rpz_txt import RecordRpzTxtResource

        return RecordRpzTxtResource(self._client)

    @cached_property
    def record_rpz_a_ipaddress(self) -> RecordRpzAIpaddressResource:
        """Entry point for NIOS RPZ A IP-address substitution resources."""
        from ibx_nios_sdk.rpz._record_rpz_a_ipaddress import RecordRpzAIpaddressResource

        return RecordRpzAIpaddressResource(self._client)

    @cached_property
    def record_rpz_aaaa_ipaddress(self) -> RecordRpzAaaaIpaddressResource:
        """Entry point for NIOS RPZ AAAA IP-address substitution resources."""
        from ibx_nios_sdk.rpz._record_rpz_aaaa_ipaddress import RecordRpzAaaaIpaddressResource

        return RecordRpzAaaaIpaddressResource(self._client)

    @cached_property
    def record_rpz_cname_ipaddress(self) -> RecordRpzCnameIpaddressResource:
        """Entry point for NIOS RPZ CNAME IP-address substitution resources."""
        from ibx_nios_sdk.rpz._record_rpz_cname_ipaddress import RecordRpzCnameIpaddressResource

        return RecordRpzCnameIpaddressResource(self._client)

    @cached_property
    def record_rpz_cname_ipaddressdn(self) -> RecordRpzCnameIpaddressdnResource:
        """Entry point for NIOS RPZ CNAME IP-address domain-name substitution resources."""
        from ibx_nios_sdk.rpz._record_rpz_cname_ipaddressdn import (
            RecordRpzCnameIpaddressdnResource,
        )

        return RecordRpzCnameIpaddressdnResource(self._client)

    @cached_property
    def record_rpz_cname_clientipaddress(self) -> RecordRpzCnameClientipaddressResource:
        """Entry point for NIOS RPZ CNAME client-IP-address substitution resources."""
        from ibx_nios_sdk.rpz._record_rpz_cname_clientipaddress import (
            RecordRpzCnameClientipaddressResource,
        )

        return RecordRpzCnameClientipaddressResource(self._client)

    @cached_property
    def record_rpz_cname_clientipaddressdn(self) -> RecordRpzCnameClientipaddressdnResource:
        """Entry point for NIOS RPZ CNAME client-IP-address domain-name substitution resources."""
        from ibx_nios_sdk.rpz._record_rpz_cname_clientipaddressdn import (
            RecordRpzCnameClientipaddressdnResource,
        )

        return RecordRpzCnameClientipaddressdnResource(self._client)

    @cached_property
    def allrpzrecords(self) -> AllrpzrecordsResource:
        """Entry point for NIOS RPZ all-records aggregate resources."""
        from ibx_nios_sdk.rpz._allrpzrecords import AllrpzrecordsResource

        return AllrpzrecordsResource(self._client)
