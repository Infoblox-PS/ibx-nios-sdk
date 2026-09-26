# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ACL domain - NIOS named ACL resources."""

from __future__ import annotations

from ibx_nios_sdk.acl._namedacl import NamedaclResource
from ibx_nios_sdk.acl._service import AclService

__all__ = [
    "AclService",
    "NamedaclResource",
]
