# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkResource - full implementation with next_available_ip function wrapper."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.network import READONLY_FIELDS, Network


class NetworkResource(WapiResource[Network]):
    """Manage NIOS IPAM IPv4 network objects with next_available_ip support."""

    _wapi_type = "network"
    _model = Network
    _default_return_fields = ["network", "network_view", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"network_view"}

    async def next_available_ip(
        self,
        ref: str,
        *,
        num: int = 1,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return the next available IP address(es) within this IPv4 network.

        Calls the WAPI ``next_available_ip`` function on the given network ref.

        Args:
            ref: The WAPI object reference for the network (e.g., ``"network/ZG5z..."``)
            num: Number of IP addresses to allocate. Defaults to 1.
            exclude: Optional list of IP addresses to exclude from consideration.

        Returns:
            A dict with key ``"ips"`` containing a list of allocated IPv4 address strings.
            Example: ``{"ips": ["192.168.1.5", "192.168.1.6"]}``

        Raises:
            WapiRequestError: If the WAPI call fails or no IPs are available.
        """
        kwargs: dict[str, Any] = {"num": num}
        if exclude is not None:
            kwargs["exclude"] = exclude
        return await self.call_function(ref, "next_available_ip", **kwargs)
