# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AclService - entry point for acl resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.acl._namedacl import NamedaclResource


class AclService:
    """Entry point for NIOS acl resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise AclService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def namedacl(self) -> NamedaclResource:
        """Entry point for NIOS named ACL resources."""
        from ibx_nios_sdk.acl._namedacl import NamedaclResource

        return NamedaclResource(self._client)
