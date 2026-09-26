# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcServer - NIOS DTC server object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "health",
        "uuid",
    }
)


class DtcServer(BaseModel):
    """NIOS DTC server."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    auto_create_host_record: bool | None = Field(
        default=None,
        description="Enabling this option will auto-create a single read-only A/AAAA/CNAME record corresponding to the configured hostname and update it if the hostname changes.",
    )
    comment: str | None = Field(
        default=None, description="Comment for the DTC Server; maximum 256 characters."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether the DTC Server is disabled or not. When this is set to False, the fixed address is enabled.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    health: dict[str, Any] | None = Field(default=None, description="Health status of the object.")
    host: str | None = Field(default=None, description="The address or FQDN of the server.")
    monitors: list[dict[str, Any]] | None = Field(
        default=None,
        description="List of IP/FQDN and monitor pairs to be used for additional monitoring.",
    )
    name: str | None = Field(default=None, description="The DTC Server display name.")
    sni_hostname: str | None = Field(
        default=None, description="The hostname for Server Name Indication (SNI) in FQDN format."
    )
    use_sni_hostname: bool | None = Field(default=None, description="Use flag for: sni_hostname")
