# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ibx-nios-sdk - async Python client for Infoblox NIOS WAPI."""

from __future__ import annotations

from ibx_nios_sdk._exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NiosConnectionError,
    NiosError,
    NotFoundError,
    RateLimitError,
    ServerError,
    UnsupportedOperationError,
    ValidationError,
)
from ibx_nios_sdk._version import __version__
from ibx_nios_sdk.acl import AclService
from ibx_nios_sdk.client import NiosClient
from ibx_nios_sdk.cloud import CloudService
from ibx_nios_sdk.dhcp import DhcpService
from ibx_nios_sdk.discovery import DiscoveryService
from ibx_nios_sdk.dns import DnsService
from ibx_nios_sdk.dtc import DtcService
from ibx_nios_sdk.federatedrealms import FederatedrealmsService
from ibx_nios_sdk.ipam import IpamService
from ibx_nios_sdk.microsoftserver import MicrosoftserverService
from ibx_nios_sdk.misc import MiscService
from ibx_nios_sdk.notification import NotificationService
from ibx_nios_sdk.rpz import RpzService
from ibx_nios_sdk.security import SecurityService
from ibx_nios_sdk.smartfolder import SmartfolderService
from ibx_nios_sdk.threatinsight import ThreatinsightService
from ibx_nios_sdk.threatprotection import ThreatprotectionService

__all__ = [
    "AclService",
    "AuthenticationError",
    "BadRequestError",
    "CloudService",
    "ConflictError",
    "DhcpService",
    "DiscoveryService",
    "MicrosoftserverService",
    "MiscService",
    "DtcService",
    "FederatedrealmsService",
    "NotificationService",
    "SmartfolderService",
    "DnsService",
    "IpamService",
    "NiosClient",
    "RpzService",
    "SecurityService",
    "ThreatinsightService",
    "ThreatprotectionService",
    "NiosConnectionError",
    "NiosError",
    "UnsupportedOperationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "__version__",
]
