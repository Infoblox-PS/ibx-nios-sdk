# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderService - entry point for Smart Folder resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.smartfolder._smartfolder_children import SmartfolderChildrenResource
    from ibx_nios_sdk.smartfolder._smartfolder_global import SmartfolderGlobalResource
    from ibx_nios_sdk.smartfolder._smartfolder_personal import SmartfolderPersonalResource


class SmartfolderService:
    """Entry point for NIOS Smart Folder resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise SmartfolderService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def children(self) -> SmartfolderChildrenResource:
        """Entry point for NIOS Smart Folder children resources."""
        from ibx_nios_sdk.smartfolder._smartfolder_children import SmartfolderChildrenResource

        return SmartfolderChildrenResource(self._client)

    @cached_property
    def global_(self) -> SmartfolderGlobalResource:
        """Entry point for NIOS global Smart Folder resources."""
        from ibx_nios_sdk.smartfolder._smartfolder_global import SmartfolderGlobalResource

        return SmartfolderGlobalResource(self._client)

    @cached_property
    def personal(self) -> SmartfolderPersonalResource:
        """Entry point for NIOS personal Smart Folder resources."""
        from ibx_nios_sdk.smartfolder._smartfolder_personal import SmartfolderPersonalResource

        return SmartfolderPersonalResource(self._client)
