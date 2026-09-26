# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneAuth resource with typed function wrappers."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.zone_auth import READONLY_FIELDS, ZoneAuth


class ZoneAuthResource(WapiResource[ZoneAuth]):
    """Manage NIOS authoritative DNS zones with copy and lock/unlock support."""

    _wapi_type = "zone_auth"
    _model = ZoneAuth
    _default_return_fields = ["fqdn", "view", "comment", "zone_format", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"fqdn", "zone_format"}

    async def copy_zone_records(
        self,
        ref: str,
        *,
        source_zone: str,
        view: str | None = None,
        copy_all_records: bool | None = None,
    ) -> dict[str, Any]:
        """WAPI function: copyzonerecords - copy records from another zone.

        Args:
            ref: The ``zone_auth`` object reference to copy records *into*.
            source_zone: FQDN of the zone to copy records *from* (WAPI field ``zone``).
            view: Optional DNS view name that scopes the source zone lookup.
            copy_all_records: When ``True``, copy all record types; default is
                False (WAPI only copies selected types).
        """
        kwargs: dict[str, Any] = {"zone": source_zone}
        if view is not None:
            kwargs["view"] = view
        if copy_all_records is not None:
            kwargs["copy_all_records"] = copy_all_records
        return await self.call_function(ref, "copyzonerecords", **kwargs)

    async def lock_unlock_zone(self, ref: str, *, lock: bool) -> dict[str, Any]:
        """WAPI function: lock_unlock_zone - lock or unlock a zone for editing.

        Args:
            ref: The ``zone_auth`` object reference.
            lock: ``True`` to lock the zone; ``False`` to unlock.
        """
        return await self.call_function(
            ref, "lock_unlock_zone", operation="LOCK" if lock else "UNLOCK"
        )
