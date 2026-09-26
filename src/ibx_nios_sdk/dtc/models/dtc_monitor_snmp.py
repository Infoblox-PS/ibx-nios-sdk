# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorSnmp - NIOS DTC SNMP monitor.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

``oids`` is an array of SNMP OID structs - modelled as
``list[dict[str, Any]] | None``. See NOTES.md.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class DtcMonitorSnmp(BaseModel):
    """NIOS DTC SNMP monitor."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    comment: str | None = Field(
        default=None, description="Comment for this DTC monitor; maximum 256 characters."
    )
    community: str | None = Field(
        default=None, description="The SNMP community string for SNMP authentication."
    )
    context: str | None = Field(default=None, description="The SNMPv3 context.")
    engine_id: str | None = Field(default=None, description="The SNMPv3 engine identifier.")
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    interval: int | None = Field(default=None, description="The interval for a health check.")
    name: str | None = Field(default=None, description="The display name for this DTC monitor.")
    oids: list[dict[str, Any]] | None = Field(
        default=None, description="A list of OIDs for SNMP monitoring."
    )
    port: int | None = Field(default=None, description="The port value for SNMP requests.")
    retry_down: int | None = Field(
        default=None,
        description="The value of how many times the server should appear as down to be treated as dead after it was alive.",
    )
    retry_up: int | None = Field(
        default=None,
        description="The value of how many times the server should appear as up to be treated as alive after it was dead.",
    )
    timeout: int | None = Field(
        default=None, description="The timeout for a health check in seconds."
    )
    user: str | None = Field(default=None, description="The SNMPv3 user setting.")
    version: Literal["V1", "V2C", "V3"] | str | None = Field(
        default=None, description="The SNMP protocol version for the SNMP health check."
    )
