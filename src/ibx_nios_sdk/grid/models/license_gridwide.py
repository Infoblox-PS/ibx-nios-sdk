# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LicenseGridwide - NIOS grid-wide license."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "expiration_status",
        "expiry_date",
        "key",
        "limit",
        "limit_context",
        "type",
        "type_",
        "uuid",
    }
)


class LicenseGridwide(BaseModel):
    """NIOS grid-wide license."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    expiration_status: (
        Literal[
            "NOT_EXPIRED", "EXPIRED", "PERMANENT", "EXPIRING_SOON", "EXPIRING_VERY_SOON", "DELETED"
        ]
        | str
        | None
    ) = Field(default=None, description="The license expiration status.")  # read-only
    expiry_date: int | None = Field(
        default=None, description="The expiration timestamp of the license."
    )  # read-only
    key: str | None = Field(default=None, description="The license string.")  # read-only
    limit: str | None = Field(default=None, description="The license limit value.")  # read-only
    limit_context: Literal["NONE", "LEASES", "MODEL", "TIER"] | str | None = Field(
        default=None, description="The license limit context."
    )  # read-only; "type" is a Python builtin - use alias
    type_: (
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
    ) = Field(default=None, alias="type", description="Object type discriminator.")

    # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
