# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightAllowlist - NIOS threat insight allowlist.

All 5 non-_ref properties from ``components.schemas.ThreatinsightAllowlist`` in the
v2.14 threatinsight swagger are represented here.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

Note: The ``name`` field listed in the plan does not exist in the swagger schema.
Default return fields are corrected to ``["fqdn", "type", "comment"]``.
``type`` shadows the Python builtin - aliased to ``type_``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "type",
        "type_",
        "uuid",
    }
)


class ThreatinsightAllowlist(BaseModel):
    """NIOS threat insight allowlist.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.

    ``type_`` aliases the JSON field ``type`` (Python builtin collision) and is
    read-only (SYSTEM | CUSTOM enum).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    type_: Literal["SYSTEM", "CUSTOM"] | str | None = Field(
        default=None, alias="type", description="Object type discriminator."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="The descriptive comment for the threat insight allowlist."
    )
    disable: bool | None = Field(
        default=None, description="Determines whether the threat insight allowlist is disabled."
    )
    fqdn: str | None = Field(default=None, description="The FQDN of the threat insight allowlist.")
