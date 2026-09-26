# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberLicense - NIOS member license.

NOTE: The ``type`` field is a Python keyword, aliased as ``type_``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "expiration_status",
        "expiry_date",
        "hwid",
        "key",
        "kind",
        "limit",
        "limit_context",
        "type",
        "type_",
        "uuid",
    }
)


class MemberLicense(BaseModel):
    """NIOS member license."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    expiration_status: (
        Literal[
            "NOT_EXPIRED", "EXPIRED", "PERMANENT", "EXPIRING_SOON", "EXPIRING_VERY_SOON", "DELETED"
        ]
        | str
        | None
    ) = Field(default=None, description="The license expiration status.")
    expiry_date: int | None = Field(
        default=None, description="The expiration timestamp of the license."
    )
    hwid: str | None = Field(
        default=None,
        description="The hardware ID of the physical node on which the license is installed.",
    )
    key: str | None = Field(default=None, description="License string.")
    kind: Literal["Static", "Dynamic", "Payg", "Gridwide"] | str | None = Field(
        default=None, description="The overall type of license: static or dynamic."
    )
    limit: str | None = Field(default=None, description="The license limit value.")
    limit_context: Literal["NONE", "LEASES", "MODEL", "TIER"] | str | None = Field(
        default=None, description="The license limit context."
    )  # read-only; aliases the WAPI "type" field (Python keyword collision)
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
