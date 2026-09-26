# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SecurityService - entry point for security resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.security._ad_auth_service import AdAuthServiceResource
    from ibx_nios_sdk.security._admingroup import AdmingroupResource
    from ibx_nios_sdk.security._adminrole import AdminroleResource
    from ibx_nios_sdk.security._adminuser import AdminuserResource
    from ibx_nios_sdk.security._approvalworkflow import ApprovalworkflowResource
    from ibx_nios_sdk.security._authpolicy import AuthpolicyResource
    from ibx_nios_sdk.security._cacertificate import CacertificateResource
    from ibx_nios_sdk.security._certificate_authservice import CertificateAuthserviceResource
    from ibx_nios_sdk.security._ftpuser import FtpuserResource
    from ibx_nios_sdk.security._hsm_allgroups import HsmAllgroupsResource
    from ibx_nios_sdk.security._hsm_entrustnshieldgroup import HsmEntrustnshieldgroupResource
    from ibx_nios_sdk.security._hsm_thaleslunagroup import HsmThaleslunagroupResource
    from ibx_nios_sdk.security._ldap_auth_service import LdapAuthServiceResource
    from ibx_nios_sdk.security._localuser_authservice import LocaluserAuthserviceResource
    from ibx_nios_sdk.security._networkuser import NetworkuserResource
    from ibx_nios_sdk.security._parentalcontrol_avp import ParentalcontrolAvpResource
    from ibx_nios_sdk.security._parentalcontrol_blockingpolicy import (
        ParentalcontrolBlockingpolicyResource,
    )
    from ibx_nios_sdk.security._parentalcontrol_subscriber import (
        ParentalcontrolSubscriberResource,
    )
    from ibx_nios_sdk.security._parentalcontrol_subscriberrecord import (
        ParentalcontrolSubscriberrecordResource,
    )
    from ibx_nios_sdk.security._parentalcontrol_subscribersite import (
        ParentalcontrolSubscribersiteResource,
    )
    from ibx_nios_sdk.security._permission import PermissionResource
    from ibx_nios_sdk.security._radius_authservice import RadiusAuthserviceResource
    from ibx_nios_sdk.security._saml_authservice import SamlAuthserviceResource
    from ibx_nios_sdk.security._snmpuser import SnmpuserResource
    from ibx_nios_sdk.security._tacacsplus_authservice import TacacsplusAuthserviceResource
    from ibx_nios_sdk.security._userprofile import UserprofileResource


class SecurityService:
    """Entry point for NIOS security resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise SecurityService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def admingroup(self) -> AdmingroupResource:
        """Entry point for NIOS admin group resources."""
        from ibx_nios_sdk.security._admingroup import AdmingroupResource

        return AdmingroupResource(self._client)

    @cached_property
    def adminrole(self) -> AdminroleResource:
        """Entry point for NIOS admin role resources."""
        from ibx_nios_sdk.security._adminrole import AdminroleResource

        return AdminroleResource(self._client)

    @cached_property
    def adminuser(self) -> AdminuserResource:
        """Entry point for NIOS admin user resources."""
        from ibx_nios_sdk.security._adminuser import AdminuserResource

        return AdminuserResource(self._client)

    @cached_property
    def permission(self) -> PermissionResource:
        """Entry point for NIOS permission resources."""
        from ibx_nios_sdk.security._permission import PermissionResource

        return PermissionResource(self._client)

    @cached_property
    def userprofile(self) -> UserprofileResource:
        """Entry point for NIOS user profile resources."""
        from ibx_nios_sdk.security._userprofile import UserprofileResource

        return UserprofileResource(self._client)

    @cached_property
    def authpolicy(self) -> AuthpolicyResource:
        """Entry point for NIOS authentication policy resources."""
        from ibx_nios_sdk.security._authpolicy import AuthpolicyResource

        return AuthpolicyResource(self._client)

    @cached_property
    def approvalworkflow(self) -> ApprovalworkflowResource:
        """Entry point for NIOS approval workflow resources."""
        from ibx_nios_sdk.security._approvalworkflow import ApprovalworkflowResource

        return ApprovalworkflowResource(self._client)

    @cached_property
    def cacertificate(self) -> CacertificateResource:
        """Entry point for NIOS CA certificate resources."""
        from ibx_nios_sdk.security._cacertificate import CacertificateResource

        return CacertificateResource(self._client)

    @cached_property
    def certificate_authservice(self) -> CertificateAuthserviceResource:
        """Entry point for NIOS certificate authentication service resources."""
        from ibx_nios_sdk.security._certificate_authservice import CertificateAuthserviceResource

        return CertificateAuthserviceResource(self._client)

    @cached_property
    def radius_authservice(self) -> RadiusAuthserviceResource:
        """Entry point for NIOS RADIUS authentication service resources."""
        from ibx_nios_sdk.security._radius_authservice import RadiusAuthserviceResource

        return RadiusAuthserviceResource(self._client)

    @cached_property
    def tacacsplus_authservice(self) -> TacacsplusAuthserviceResource:
        """Entry point for NIOS TACACS+ authentication service resources."""
        from ibx_nios_sdk.security._tacacsplus_authservice import TacacsplusAuthserviceResource

        return TacacsplusAuthserviceResource(self._client)

    @cached_property
    def ldap_auth_service(self) -> LdapAuthServiceResource:
        """Entry point for NIOS LDAP authentication service resources."""
        from ibx_nios_sdk.security._ldap_auth_service import LdapAuthServiceResource

        return LdapAuthServiceResource(self._client)

    @cached_property
    def saml_authservice(self) -> SamlAuthserviceResource:
        """Entry point for NIOS SAML authentication service resources."""
        from ibx_nios_sdk.security._saml_authservice import SamlAuthserviceResource

        return SamlAuthserviceResource(self._client)

    @cached_property
    def localuser_authservice(self) -> LocaluserAuthserviceResource:
        """Entry point for NIOS local-user authentication service resources."""
        from ibx_nios_sdk.security._localuser_authservice import LocaluserAuthserviceResource

        return LocaluserAuthserviceResource(self._client)

    @cached_property
    def ad_auth_service(self) -> AdAuthServiceResource:
        """Entry point for NIOS Active Directory authentication service resources."""
        from ibx_nios_sdk.security._ad_auth_service import AdAuthServiceResource

        return AdAuthServiceResource(self._client)

    @cached_property
    def snmpuser(self) -> SnmpuserResource:
        """Entry point for NIOS SNMP user resources."""
        from ibx_nios_sdk.security._snmpuser import SnmpuserResource

        return SnmpuserResource(self._client)

    @cached_property
    def ftpuser(self) -> FtpuserResource:
        """Entry point for NIOS FTP user resources."""
        from ibx_nios_sdk.security._ftpuser import FtpuserResource

        return FtpuserResource(self._client)

    @cached_property
    def networkuser(self) -> NetworkuserResource:
        """Entry point for NIOS network user resources."""
        from ibx_nios_sdk.security._networkuser import NetworkuserResource

        return NetworkuserResource(self._client)

    @cached_property
    def hsm_allgroups(self) -> HsmAllgroupsResource:
        """Entry point for NIOS HSM all-groups resources."""
        from ibx_nios_sdk.security._hsm_allgroups import HsmAllgroupsResource

        return HsmAllgroupsResource(self._client)

    @cached_property
    def hsm_entrustnshieldgroup(self) -> HsmEntrustnshieldgroupResource:
        """Entry point for NIOS HSM Entrust nShield group resources."""
        from ibx_nios_sdk.security._hsm_entrustnshieldgroup import HsmEntrustnshieldgroupResource

        return HsmEntrustnshieldgroupResource(self._client)

    @cached_property
    def hsm_thaleslunagroup(self) -> HsmThaleslunagroupResource:
        """Entry point for NIOS HSM Thales Luna group resources."""
        from ibx_nios_sdk.security._hsm_thaleslunagroup import HsmThaleslunagroupResource

        return HsmThaleslunagroupResource(self._client)

    @cached_property
    def parentalcontrol_avp(self) -> ParentalcontrolAvpResource:
        """Entry point for NIOS parental-control AVP resources."""
        from ibx_nios_sdk.security._parentalcontrol_avp import ParentalcontrolAvpResource

        return ParentalcontrolAvpResource(self._client)

    @cached_property
    def parentalcontrol_blockingpolicy(self) -> ParentalcontrolBlockingpolicyResource:
        """Entry point for NIOS parental-control blocking policy resources."""
        from ibx_nios_sdk.security._parentalcontrol_blockingpolicy import (
            ParentalcontrolBlockingpolicyResource,
        )

        return ParentalcontrolBlockingpolicyResource(self._client)

    @cached_property
    def parentalcontrol_subscriber(self) -> ParentalcontrolSubscriberResource:
        """Entry point for NIOS parental-control subscriber resources."""
        from ibx_nios_sdk.security._parentalcontrol_subscriber import (
            ParentalcontrolSubscriberResource,
        )

        return ParentalcontrolSubscriberResource(self._client)

    @cached_property
    def parentalcontrol_subscriberrecord(self) -> ParentalcontrolSubscriberrecordResource:
        """Entry point for NIOS parental-control subscriber record resources."""
        from ibx_nios_sdk.security._parentalcontrol_subscriberrecord import (
            ParentalcontrolSubscriberrecordResource,
        )

        return ParentalcontrolSubscriberrecordResource(self._client)

    @cached_property
    def parentalcontrol_subscribersite(self) -> ParentalcontrolSubscribersiteResource:
        """Entry point for NIOS parental-control subscriber site resources."""
        from ibx_nios_sdk.security._parentalcontrol_subscribersite import (
            ParentalcontrolSubscribersiteResource,
        )

        return ParentalcontrolSubscribersiteResource(self._client)
