# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkcontainerResource - full implementation with next_available_network wrapper."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.networkcontainer import READONLY_FIELDS, Networkcontainer


class NetworkcontainerResource(WapiResource[Networkcontainer]):
    """Manage NIOS IPAM IPv4 network containers with next_available_network support."""

    _wapi_type = "networkcontainer"
    _model = Networkcontainer
    _default_return_fields = ["network", "network_view", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"network_view"}

    async def next_available_network(
        self,
        ref: str,
        *,
        cidr: int,
        num: int = 1,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """Carve out the next available network(s) from this IPv4 container.

        Calls the WAPI ``next_available_network`` function on the given container ref.

        Args:
            ref: The WAPI object reference for the network container
                (e.g., ``"networkcontainer/ZG5z..."``)
            cidr: The prefix length for the new network (e.g., 24 for /24).
            num: Number of networks to allocate. Defaults to 1.
            exclude: Optional list of network CIDRs to exclude from consideration.

        Returns:
            A dict with key ``"networks"`` containing a list of allocated CIDR strings.
            Example: ``{"networks": ["10.0.0.0/24", "10.0.1.0/24"]}``

        Raises:
            WapiRequestError: If the WAPI call fails or no networks are available.
        """
        kwargs: dict[str, Any] = {"cidr": cidr, "num": num}
        if exclude is not None:
            kwargs["exclude"] = exclude
        return await self.call_function(ref, "next_available_network", **kwargs)
