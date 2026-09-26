# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridLicensePool - NIOS Grid license pool."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "assigned",
        "expiration_status",
        "expiry_date",
        "installed",
        "key",
        "limit",
        "limit_context",
        "model",
        "subpools",
        "temp_assigned",
        "type",
        "uuid",
    }
)


class GridLicensePool(BaseModel):
    """NIOS Grid license pool."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    assigned: int | None = Field(
        default=None, description="The number of dynamic licenses allocated to vNIOS appliances."
    )  # read-only
    expiration_status: (
        Literal[
            "NOT_EXPIRED", "EXPIRED", "PERMANENT", "EXPIRING_SOON", "EXPIRING_VERY_SOON", "DELETED"
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="The license expiration status. * DELETED - The temporary license has been deleted. * EXPIRED - License/Pool has reached the expiry date. * EXPIRING_SOON - License/Pool expires in 31-90 days. * EXPIRING_VERY_SOON - License/Pool expires in 30 days or earlier. * NOT_EXPIRED - License/Pool has not expired. * PERMANENT - License/Pool does not expire.",
    )  # read-only
    expiry_date: int | None = Field(
        default=None, description="The expiration timestamp of the license."
    )  # read-only
    installed: int | None = Field(
        default=None,
        description="The total number of dynamic licenses allowed for this license pool.",
    )  # read-only
    key: str | None = Field(
        default=None, description="The license string for the license pool."
    )  # read-only
    limit: str | None = Field(
        default=None,
        description="The limitation of dynamic license that can be allocated from the license pool.",
    )  # read-only
    limit_context: Literal["NONE", "LEASES", "MODEL", "TIER"] | str | None = Field(
        default=None, description="The license limit context."
    )  # read-only
    model: str | None = Field(
        default=None, description="The supported vNIOS virtual appliance model."
    )  # read-only
    subpools: list[dict[str, object]] | None = Field(
        default=None, description="The license pool subpools."
    )  # read-only
    temp_assigned: int | None = Field(
        default=None,
        description="The total number of temporary dynamic licenses allocated to vNIOS appliances.",
    )  # read-only (type is a Python builtin but not a keyword, can use directly)
    type: (
        Literal[
            "ANYCAST",
            "CLOUD",
            "CLOUD_API",
            "DCA",
            "DDI_TRIAL",
            "DHCP",
            "DISCOVERY",
            "DNS",
            "DNSQRW",
            "DNS_CACHE_ACCEL",
            "DTC",
            "FIREEYE",
            "FLEX_GRID_ACTIVATION",
            "FLEX_GRID_ACTIVATION_MS",
            "FREQ_CONTROL",
            "GRID",
            "GRID_MAINTENANCE",
            "IPAM",
            "IPAM_FREEWARE",
            "LDAP",
            "LOAD_BALANCER",
            "MGM",
            "MSMGMT",
            "NIOS",
            "NIOS_MAINTENANCE",
            "NTP",
            "OEM",
            "QRD",
            "REPORTING",
            "REPORTING_SUB",
            "RPZ",
            "SECURITY_ECOSYSTEM",
            "SW_TP",
            "TAE",
            "TFTP",
            "THREAT_INSIGHT",
            "TP",
            "TP_SUB",
            "VNIOS",
        ]
        | str
        | None
    ) = Field(default=None, description="The license type.")  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
