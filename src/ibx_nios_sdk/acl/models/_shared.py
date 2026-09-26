# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Shared nested-type models used across acl resources."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class _AclNested(BaseModel):
    """Base for acl nested types: permissive, name-aware, no _ref."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")
