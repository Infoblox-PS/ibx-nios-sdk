# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverAdsitesDomain - NIOS MS server AD sites domain (read-only).

Operations: GET (collection and by ref) only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "ea_definition",
        "ms_sync_master_name",
        "name",
        "netbios",
        "network_view",
        "read_only",
        "uuid",
    }
)


class MsserverAdsitesDomain(BaseModel):
    """NIOS MS server AD sites domain - read-only aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    ea_definition: str | None = Field(
        default=None,
        description="The name of the Extensible Attribute Definition object that is linked to the Active Directory Sites Domain.",
    )
    ms_sync_master_name: str | None = Field(
        default=None,
        description="The IP address or FQDN of the managing master for the MS server, if applicable.",
    )
    name: str | None = Field(
        default=None, description="The name of the Active Directory Domain properties object."
    )
    netbios: str | None = Field(
        default=None,
        description="The NetBIOS name of the Active Directory Domain properties object.",
    )
    network_view: str | None = Field(
        default=None,
        description="The name of the network view in which the Active Directory Domain resides.",
    )
    read_only: bool | None = Field(
        default=None,
        description="Determines whether the Active Directory Domain properties object is a read-only object.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
