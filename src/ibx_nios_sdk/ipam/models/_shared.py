# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Shared base types for IPAM models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class _IpamNested(BaseModel):
    """Base class for nested IPAM model types."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")
