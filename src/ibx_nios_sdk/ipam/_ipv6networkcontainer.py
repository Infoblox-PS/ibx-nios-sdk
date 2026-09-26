# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6networkcontainerResource - full implementation with next_available_network wrapper."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.ipv6networkcontainer import READONLY_FIELDS, Ipv6networkcontainer


class Ipv6networkcontainerResource(WapiResource[Ipv6networkcontainer]):
    """Manage NIOS IPAM IPv6 network containers with next_available_network support."""

    _wapi_type = "ipv6networkcontainer"
    _model = Ipv6networkcontainer
    _default_return_fields = ["network", "network_view", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"auto_create_reversezone"}

    async def next_available_network(
        self,
        ref: str,
        *,
        cidr: int,
        num: int = 1,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """Carve out the next available IPv6 network(s) from this IPv6 container.

        Calls the WAPI ``next_available_network`` function on the given container ref.

        Args:
            ref: The WAPI object reference for the IPv6 network container
                (e.g., ``"ipv6networkcontainer/ZG5z..."``)
            cidr: The prefix length for the new IPv6 network (e.g., 64 for /64).
            num: Number of networks to allocate. Defaults to 1.
            exclude: Optional list of IPv6 network CIDRs to exclude from consideration.

        Returns:
            A dict with key ``"networks"`` containing a list of allocated IPv6 CIDR strings.
            Example: ``{"networks": ["2001:db8::/64", "2001:db8:0:1::/64"]}``

        Raises:
            WapiRequestError: If the WAPI call fails or no networks are available.
        """
        kwargs: dict[str, Any] = {"cidr": cidr, "num": num}
        if exclude is not None:
            kwargs["exclude"] = exclude
        return await self.call_function(ref, "next_available_network", **kwargs)
