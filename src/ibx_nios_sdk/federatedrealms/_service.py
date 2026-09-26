# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FederatedrealmsService - entry point for federated realms resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.federatedrealms._federatedrealms import FederatedrealmsResource
    from ibx_nios_sdk.federatedrealms._fedipamop import FedipamopResource


class FederatedrealmsService:
    """Entry point for NIOS federated realms resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise FederatedrealmsService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def federatedrealms(self) -> FederatedrealmsResource:
        """Entry point for NIOS federated realms configuration resources."""
        from ibx_nios_sdk.federatedrealms._federatedrealms import FederatedrealmsResource

        return FederatedrealmsResource(self._client)

    @cached_property
    def fedipamop(self) -> FedipamopResource:
        """Entry point for NIOS federated IPAM operation resources."""
        from ibx_nios_sdk.federatedrealms._fedipamop import FedipamopResource

        return FedipamopResource(self._client)
