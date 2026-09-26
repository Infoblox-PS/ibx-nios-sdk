# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorSip - NIOS DTC SIP monitor.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class DtcMonitorSip(BaseModel):
    """NIOS DTC SIP monitor."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    ciphers: str | None = Field(
        default=None, description="An optional cipher list for secure TLS/SIPS connection."
    )
    client_cert: str | None = Field(
        default=None,
        description="An optional client certificate, supplied in TLS and SIPS mode if present.",
    )
    comment: str | None = Field(
        default=None, description="Comment for this DTC monitor; maximum 256 characters."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    interval: int | None = Field(default=None, description="The interval for a health check.")
    name: str | None = Field(default=None, description="The display name for this DTC monitor.")
    port: int | None = Field(default=None, description="The port value for SIP requests.")
    request: str | None = Field(default=None, description="A SIP request to send")
    result: Literal["ANY", "CODE_IS", "CODE_IS_NOT"] | str | None = Field(
        default=None, description="The type of an expected result."
    )
    result_code: int | None = Field(default=None, description="The expected return code value.")
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
    transport: Literal["TCP", "SIPS", "TLS", "UDP"] | str | None = Field(
        default=None, description="The transport layer protocol to use for SIP check."
    )
    validate_cert: bool | None = Field(
        default=None,
        description="Determines whether the validation of the remote server's certificate is enabled.",
    )
