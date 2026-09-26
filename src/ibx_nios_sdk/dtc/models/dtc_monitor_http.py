# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorHttp - NIOS DTC HTTP monitor.

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


class DtcMonitorHttp(BaseModel):
    """NIOS DTC HTTP monitor."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    ciphers: str | None = Field(
        default=None, description="An optional cipher list for a secure HTTP/S connection."
    )
    client_cert: str | None = Field(
        default=None,
        description="An optional client certificate, supplied in a secure HTTP/S mode if present.",
    )
    comment: str | None = Field(
        default=None, description="Comment for this DTC monitor; maximum 256 characters."
    )
    content_check: Literal["NONE", "MATCH", "EXTRACT"] | str | None = Field(
        default=None, description="The content check type."
    )
    content_check_input: Literal["HEADERS", "ALL", "BODY"] | str | None = Field(
        default=None, description="A portion of response to use as input for content check."
    )
    content_check_op: Literal["EQ", "NEQ", "LEQ", "GEQ"] | str | None = Field(
        default=None, description="A content check success criteria operator."
    )
    content_check_regex: str | None = Field(
        default=None, description="A content check regular expression."
    )
    content_extract_group: int | None = Field(
        default=None, description="A content extraction sub-expression to extract."
    )
    content_extract_type: Literal["STRING", "INTEGER"] | str | None = Field(
        default=None, description="A content extraction expected type for the extracted data."
    )
    content_extract_value: str | None = Field(
        default=None, description="A content extraction value to compare with extracted result."
    )
    enable_sni: bool | None = Field(
        default=None,
        description="Determines whether the Server Name Indication (SNI) for HTTPS monitor is enabled.",
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    interval: int | None = Field(default=None, description="The interval for a health check.")
    name: str | None = Field(default=None, description="The display name for this DTC monitor.")
    port: int | None = Field(default=None, description="Port for TCP requests.")
    request: str | None = Field(default=None, description="An HTTP request to send.")
    result: Literal["ANY", "CODE_IS", "CODE_IS_NOT"] | str | None = Field(
        default=None, description="The type of an expected result."
    )
    result_code: int | None = Field(default=None, description="The expected return code.")
    retry_down: int | None = Field(
        default=None,
        description="The value of how many times the server should appear as down to be treated as dead after it was alive.",
    )
    retry_up: int | None = Field(
        default=None,
        description="The value of how many times the server should appear as up to be treated as alive after it was dead.",
    )
    secure: bool | None = Field(default=None, description="The connection security status.")
    timeout: int | None = Field(
        default=None, description="The timeout for a health check in seconds."
    )
    validate_cert: bool | None = Field(
        default=None,
        description="Determines whether the validation of the remote server's certificate is enabled.",
    )
