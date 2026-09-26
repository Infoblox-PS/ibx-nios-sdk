# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6rangeResource - DHCP IPv6 range with next_available_ip typed wrapper."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6range import READONLY_FIELDS, Ipv6range


class Ipv6rangeResource(WapiResource[Ipv6range]):
    """Manage NIOS DHCPv6 range objects with next_available_ip support."""

    _wapi_type = "ipv6range"
    _model = Ipv6range
    _default_return_fields = [
        "start_addr",
        "end_addr",
        "network",
        "network_view",
        "comment",
        "disable",
    ]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"template"}

    async def next_available_ip(
        self,
        ref: str,
        *,
        num: int = 1,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return the next available IPv6 address(es) within this DHCPv6 range.

        Calls the WAPI ``next_available_ip`` function on the given IPv6 range ref.

        Args:
            ref: The WAPI object reference for the DHCPv6 range
                (e.g., ``"ipv6range/ZG5z..."``)
            num: Number of IPv6 addresses to allocate. Defaults to 1.
            exclude: Optional list of IPv6 addresses to exclude from consideration.

        Returns:
            A dict with key ``"ips"`` containing a list of allocated IPv6 address strings.
            Example: ``{"ips": ["2001:db8::100", "2001:db8::101"]}``

        Raises:
            WapiRequestError: If the WAPI call fails or no IPs are available.
        """
        kwargs: dict[str, Any] = {"num": num}
        if exclude is not None:
            kwargs["exclude"] = exclude
        return await self.call_function(ref, "next_available_ip", **kwargs)
