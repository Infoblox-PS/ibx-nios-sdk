# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""IPAM domain pydantic models."""

from __future__ import annotations

from ibx_nios_sdk.ipam.models.ipv4address import Ipv4address
from ibx_nios_sdk.ipam.models.network import Network
from ibx_nios_sdk.ipam.models.networkcontainer import Networkcontainer
from ibx_nios_sdk.ipam.models.networktemplate import Networktemplate
from ibx_nios_sdk.ipam.models.networkview import Networkview
from ibx_nios_sdk.ipam.models.rir import Rir
from ibx_nios_sdk.ipam.models.rir_organization import RirOrganization

__all__: list[str] = [
    "Ipv4address",
    "Network",
    "Networkcontainer",
    "Networktemplate",
    "Networkview",
    "Rir",
    "RirOrganization",
]
