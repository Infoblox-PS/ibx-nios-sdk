# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberResource - NIOS Grid member."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member import READONLY_FIELDS, Member


class MemberResource(WapiResource[Member]):
    """Manage NIOS Grid member objects with restart_services support."""

    _wapi_type = "member"
    _model = Member
    _default_return_fields = [
        "host_name",
        "config_addr_type",
        "platform",
        "service_type_configuration",
        "comment",
    ]
    _readonly_fields = set(READONLY_FIELDS)

    async def restart_services(
        self,
        ref: str,
        *,
        services: list[str] | None = None,
        restart_option: str = "RESTART_IF_NEEDED",
    ) -> dict[str, Any]:
        """Restart NIOS services on this Grid member.

        Calls the WAPI ``restartservices`` function on the member ref.

        Args:
            ref: The WAPI object reference for the Grid member
                (e.g., ``"member/ZG5z..."``)
            services: Optional list of service names to restart. If not provided,
                all services on the member are restarted.
            restart_option: Restart trigger policy. One of
                ``"RESTART_IF_NEEDED"`` (default), ``"FORCE_RESTART"``,
                ``"RELOAD_ALL"``, ``"RESTART_ALL"``.

        Returns:
            A dict containing the WAPI function response, typically empty on success.

        Raises:
            WapiRequestError: If the WAPI call fails or the member ref is invalid.
        """
        kwargs: dict[str, Any] = {"restart_option": restart_option}
        if services is not None:
            kwargs["services"] = services
        return await self.call_function(ref, "restartservices", **kwargs)
