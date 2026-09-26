# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartGroupResource - NIOS Grid service-restart group."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_servicerestart_group import (
    READONLY_FIELDS,
    GridServicerestartGroup,
)


class GridServicerestartGroupResource(WapiResource[GridServicerestartGroup]):
    """Manage NIOS Grid service-restart group objects with restart_services support."""

    _wapi_type = "grid:servicerestart:group"
    _model = GridServicerestartGroup
    _default_return_fields = ["name", "comment", "service", "mode"]
    _readonly_fields = set(READONLY_FIELDS)

    async def restart_services(
        self,
        ref: str,
        *,
        services: list[str] | None = None,
        restart_option: str = "RESTART_IF_NEEDED",
    ) -> dict[str, Any]:
        """Restart NIOS services in this service-restart group.

        Calls the WAPI ``restart`` function on the service-restart group ref.

        Args:
            ref: The WAPI object reference for the service-restart group
                (e.g., ``"grid:servicerestart:group/ZG5z..."``)
            services: Optional list of service names to restart. If not provided,
                all services in the group are restarted.
            restart_option: Restart trigger policy. One of
                ``"RESTART_IF_NEEDED"`` (default), ``"FORCE_RESTART"``,
                ``"RELOAD_ALL"``, ``"RESTART_ALL"``.

        Returns:
            A dict containing the WAPI function response, typically empty on success.

        Raises:
            WapiRequestError: If the WAPI call fails or the group ref is invalid.
        """
        kwargs: dict[str, Any] = {"restart_option": restart_option}
        if services is not None:
            kwargs["services"] = services
        return await self.call_function(ref, "restart", **kwargs)
