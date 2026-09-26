# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6networkResource - full implementation with next_available_ip function wrapper."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.ipv6network import READONLY_FIELDS, Ipv6network


class Ipv6networkResource(WapiResource[Ipv6network]):
    """Manage NIOS IPAM IPv6 network objects with next_available_ip support."""

    _wapi_type = "ipv6network"
    _model = Ipv6network
    _default_return_fields = ["network", "network_view", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"auto_create_reversezone", "template"}

    async def next_available_ip(
        self,
        ref: str,
        *,
        num: int = 1,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return the next available IPv6 address(es) within this IPv6 network.

        Calls the WAPI ``next_available_ip`` function on the given IPv6 network ref.

        Args:
            ref: The WAPI object reference for the IPv6 network
                (e.g., ``"ipv6network/ZG5z..."``)
            num: Number of IPv6 addresses to allocate. Defaults to 1.
            exclude: Optional list of IPv6 addresses to exclude from consideration.

        Returns:
            A dict with key ``"ips"`` containing a list of allocated IPv6 address strings.
            Example: ``{"ips": ["2001:db8::5", "2001:db8::6"]}``

        Raises:
            WapiRequestError: If the WAPI call fails or no IPs are available.
        """
        kwargs: dict[str, Any] = {"num": num}
        if exclude is not None:
            kwargs["exclude"] = exclude
        return await self.call_function(ref, "next_available_ip", **kwargs)
