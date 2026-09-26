# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RangeResource - DHCP IPv4 range with next_available_ip typed wrapper."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.range import READONLY_FIELDS, Range


class RangeResource(WapiResource[Range]):
    """Manage NIOS DHCP IPv4 range objects with next_available_ip support."""

    _wapi_type = "range"
    _model = Range
    _default_return_fields = [
        "start_addr",
        "end_addr",
        "network",
        "network_view",
        "comment",
        "disable",
    ]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"split_member", "split_scope_exclusion_percent", "template"}

    async def next_available_ip(
        self,
        ref: str,
        *,
        num: int = 1,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return the next available IP address(es) within this DHCP range.

        Calls the WAPI ``next_available_ip`` function on the given range ref.

        Args:
            ref: The WAPI object reference for the DHCP range
                (e.g., ``"range/ZG5z..."``)
            num: Number of IP addresses to allocate. Defaults to 1.
            exclude: Optional list of IP addresses to exclude from consideration.

        Returns:
            A dict with key ``"ips"`` containing a list of allocated IPv4 address strings.
            Example: ``{"ips": ["192.168.1.100", "192.168.1.101"]}``

        Raises:
            WapiRequestError: If the WAPI call fails or no IPs are available.
        """
        kwargs: dict[str, Any] = {"num": num}
        if exclude is not None:
            kwargs["exclude"] = exclude
        return await self.call_function(ref, "next_available_ip", **kwargs)
