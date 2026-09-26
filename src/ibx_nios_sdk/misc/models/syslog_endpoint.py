# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SyslogEndpoint - NIOS syslog endpoint object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
Function: POST /syslog:endpoint/{ref}/test_syslog_connection.

WAPI type: syslog:endpoint

NOTES:
- 'uuid' is read-only.
- 'syslog_servers' is a list of nested objects; typed as list[dict[str, Any]] | None.
- 'template_instance' and 'test_syslog_connection' are deeply-nested;
  typed as dict[str, Any] | None.
- 'outbound_members' is a list field.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class SyslogEndpoint(BaseModel):
    """NIOS syslog endpoint."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    log_level: Literal["ERROR", "WARNING", "INFO", "DEBUG"] | str | None = Field(
        default=None, description="The log level for a notification REST endpoint."
    )
    name: str | None = Field(default=None, description="The name of a Syslog endpoint.")
    outbound_member_type: Literal["MEMBER", "GM"] | str | None = Field(
        default=None, description="The outbound member that will generate events."
    )
    outbound_members: list[str] | None = Field(
        default=None, description="The list of members for outbound events."
    )
    syslog_servers: list[dict[str, Any]] | None = Field(
        default=None, description="List of syslog servers"
    )
    template_instance: dict[str, Any] | None = Field(
        default=None, description="Reference to the template this object was instantiated from."
    )
    test_syslog_connection: dict[str, Any] | None = Field(default=None)
    timeout: int | None = Field(
        default=None, description="The timeout of session management (in seconds)."
    )
    vendor_identifier: str | None = Field(default=None, description="The vendor identifier.")
    wapi_user_name: str | None = Field(
        default=None, description="The user name for WAPI integration."
    )
    wapi_user_password: str | None = Field(
        default=None, description="The user password for WAPI integration."
    )
