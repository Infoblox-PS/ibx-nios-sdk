# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridResource - NIOS Grid object."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid import READONLY_FIELDS, Grid


class GridResource(WapiResource[Grid]):
    """Manage the NIOS Grid object with restart_services support."""

    _wapi_type = "grid"
    _model = Grid
    _default_return_fields = ["name"]
    _readonly_fields = set(READONLY_FIELDS)

    async def restart_services(
        self,
        ref: str,
        *,
        member_order: str = "SIMULTANEOUSLY",
        restart_option: str = "RESTART_IF_NEEDED",
        services: list[str] | None = None,
    ) -> dict[str, Any]:
        """Restart NIOS services across all Grid members.

        Calls the WAPI ``restartservices`` function on the Grid object ref.

        Args:
            ref: The WAPI object reference for the Grid object
                (e.g., ``"grid/b25lLmNs..."``)
            member_order: Order in which members restart services. One of
                ``"SIMULTANEOUSLY"`` (default), ``"SEQUENTIALLY"``.
            restart_option: Restart trigger policy. One of
                ``"RESTART_IF_NEEDED"`` (default), ``"FORCE_RESTART"``,
                ``"RELOAD_ALL"``, ``"RESTART_ALL"``.
            services: Optional list of service names to restart. If not provided,
                all services are restarted.

        Returns:
            A dict containing the WAPI function response, typically empty on success.

        Raises:
            WapiRequestError: If the WAPI call fails or the Grid ref is invalid.
        """
        kwargs: dict[str, Any] = {
            "member_order": member_order,
            "restart_option": restart_option,
        }
        if services is not None:
            kwargs["services"] = services
        return await self.call_function(ref, "restartservices", **kwargs)
