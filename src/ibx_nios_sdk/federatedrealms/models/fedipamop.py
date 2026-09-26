# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Fedipamop - NIOS federated IPAM operation object.

Operations: GET collection, GET by ref, PUT (no POST, no DELETE).

NOTE: The 'get_ancestor_federated_realms' field contains nested data and is
represented as dict[str, Any] | None. See NOTES.md.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset()


class Fedipamop(BaseModel):
    """NIOS federated IPAM operation.

    NOTES:
    - 'get_ancestor_federated_realms' is a deeply-nested structure; typed as
      dict[str, Any] | None.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable ---
    get_ancestor_federated_realms: dict[str, Any] | None = Field(default=None)
