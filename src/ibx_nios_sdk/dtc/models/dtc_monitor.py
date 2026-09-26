# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitor - NIOS DTC base monitor type.

Operations: GET collection, GET by ref, PUT (no POST or DELETE).

``type`` is a Python keyword collision - aliased as ``type_``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# No readOnly fields in DtcMonitor schema
READONLY_FIELDS: frozenset[str] = frozenset()


class DtcMonitor(BaseModel):
    """NIOS DTC base monitor - read/update only.

    ``type`` (Python keyword collision) is exposed as ``type_`` with
    ``Field(alias="type")``.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    comment: str | None = Field(
        default=None, description="Comment for this DTC monitor; maximum 256 characters."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    interval: int | None = Field(default=None, description="The interval for a health check.")
    monitor: str | None = Field(default=None, description="The actual monitor object.")
    name: str | None = Field(default=None, description="The display name for this DTC monitor.")
    port: int | None = Field(default=None, description="The health monitor port value.")
    retry_down: int | None = Field(
        default=None,
        description='The number of how many times the server should appear as "DOWN" to be treated as dead after it was alive.',
    )
    retry_up: int | None = Field(
        default=None,
        description='The number of many times the server should appear as "UP" to be treated as alive after it was dead.',
    )
    timeout: int | None = Field(
        default=None, description="The timeout for a health check."
    )  # Python keyword collision: type → type_
    type_: Literal["HTTP", "ICMP", "TCP", "PDP", "SIP", "SNMP"] | str | None = Field(
        default=None, alias="type", description="Object type discriminator."
    )
